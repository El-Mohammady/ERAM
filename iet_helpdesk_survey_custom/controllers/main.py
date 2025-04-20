# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from odoo import fields, http, _
from odoo.http import request, content_disposition
from odoo.tools import format_datetime, format_date, is_html_empty

_logger = logging.getLogger(__name__)


class SurveyInherit(http.Controller):

    def _get_access_data(self, survey_token, answer_token, ensure_token=True, check_partner=True):
        """ Get back data related to survey and user input, given the ID and access
        token provided by the route.

         : param ensure_token: whether user input existence should be enforced or not(see ``_check_validity``)
         : param check_partner: whether the partner of the target answer should be checked (see ``_check_validity``)
        """
        survey_sudo, answer_sudo = request.env['survey.survey'].sudo(), request.env['survey.user_input'].sudo()
        has_survey_access, can_answer = False, False

        validity_code = self._check_validity(survey_token, answer_token, ensure_token=ensure_token, check_partner=check_partner)
        if validity_code != 'survey_wrong':
            survey_sudo, answer_sudo = self._fetch_from_access_token(survey_token, answer_token)
            has_survey_access = survey_sudo.with_user(request.env.user).has_access('read')
            can_answer = bool(answer_sudo)
            if not can_answer:
                can_answer = survey_sudo.access_mode == 'public'

        return {
            'survey_sudo': survey_sudo,
            'answer_sudo': answer_sudo,
            'has_survey_access': has_survey_access,
            'can_answer': can_answer,
            'validity_code': validity_code,
        }

    def _check_validity(self, survey_token, answer_token, ensure_token=True, check_partner=True):
        """ Check survey is open and can be taken. This does not checks for
        security rules, only functional / business rules. It returns a string key
        allowing further manipulation of validity issues

         * survey_wrong: survey does not exist;
         * survey_auth: authentication is required;
         * survey_closed: survey is closed and does not accept input anymore;
         * survey_void: survey is void and should not be taken;
         * token_wrong: given token not recognized;
         * token_required: no token given although it is necessary to access the
           survey;
         * answer_deadline: token linked to an expired answer;

        :param ensure_token: whether user input existence based on given access token
          should be enforced or not, depending on the route requesting a token or
          allowing external world calls;

        :param check_partner: Whether we must check that the partner associated to the target
          answer corresponds to the active user.
        """
        survey_sudo, answer_sudo = self._fetch_from_access_token(survey_token, answer_token)

        if not survey_sudo.exists():
            return 'survey_wrong'

        if answer_token and not answer_sudo:
            return 'token_wrong'

        if not answer_sudo and ensure_token:
            return 'token_required'
        if not answer_sudo and survey_sudo.access_mode == 'token':
            return 'token_required'

        if survey_sudo.users_login_required and request.env.user._is_public():
            return 'survey_auth'

        if not survey_sudo.active and (not answer_sudo or not answer_sudo.test_entry):
            return 'survey_closed'

        if (not survey_sudo.page_ids and survey_sudo.questions_layout == 'page_per_section') or not survey_sudo.question_ids:
            return 'survey_void'

        if answer_sudo and answer_sudo.deadline and answer_sudo.deadline < datetime.now():
            return 'answer_deadline'

        if answer_sudo and check_partner:
            if request.env.user._is_public() and answer_sudo.partner_id and not answer_token:
                # answers from public user should not have any partner_id; this indicates probably a cookie issue
                return 'answer_wrong_user'
            if not request.env.user._is_public() and answer_sudo.partner_id != request.env.user.partner_id:
                # partner mismatch, probably a cookie issue
                return 'answer_wrong_user'

        return True

    def _fetch_from_access_token(self, survey_token, answer_token):
        """ Check that given token matches an answer from the given survey_id.
        Returns a sudo-ed browse record of survey in order to avoid access rights
        issues now that access is granted through token. """
        survey_sudo = request.env['survey.survey'].with_context(active_test=False).sudo().search([('access_token', '=', survey_token)])
        if not answer_token:
            answer_sudo = request.env['survey.user_input'].sudo()
        else:
            answer_sudo = request.env['survey.user_input'].sudo().search([
                ('survey_id', '=', survey_sudo.id),
                ('access_token', '=', answer_token)
            ], limit=1)
        return survey_sudo, answer_sudo

    def _extract_comment_from_answers(self, question, answers):
        """ Answers is a custom structure depending of the question type
        that can contain question answers but also comments that need to be
        extracted before validating and saving answers.
        If multiple answers, they are listed in an array, except for matrix
        where answers are structured differently. See input and output for
        more info on data structures.
        :param question: survey.question
        :param answers:
          * question_type: free_text, text_box, numerical_box, date, datetime
            answers is a string containing the value
          * question_type: simple_choice with no comment
            answers is a string containing the value ('question_id_1')
          * question_type: simple_choice with comment
            ['question_id_1', {'comment': str}]
          * question_type: multiple choice
            ['question_id_1', 'question_id_2'] + [{'comment': str}] if holds a comment
          * question_type: matrix
            {'matrix_row_id_1': ['question_id_1', 'question_id_2'],
             'matrix_row_id_2': ['question_id_1', 'question_id_2']
            } + {'comment': str} if holds a comment
        :return: tuple(
          same structure without comment,
          extracted comment for given question
        ) """
        comment = None
        answers_no_comment = []
        if answers:
            if question.question_type == 'matrix':
                if 'comment' in answers:
                    comment = answers['comment'].strip()
                    answers.pop('comment')
                answers_no_comment = answers
            else:
                if not isinstance(answers, list):
                    answers = [answers]
                for answer in answers:
                    if isinstance(answer, dict) and 'comment' in answer:
                        comment = answer['comment'].strip()
                    else:
                        answers_no_comment.append(answer)
                if len(answers_no_comment) == 1:
                    answers_no_comment = answers_no_comment[0]
        return answers_no_comment, comment

    def _prepare_question_html(self, survey_sudo, answer_sudo, **post):
        """ Survey page navigation is done in AJAX. This function prepare the 'next page' to display in html
        and send back this html to the survey_form widget that will inject it into the page.
        Background url must be given to the caller in order to process its refresh as we don't have the next question
        object at frontend side."""
        survey_data = self._prepare_survey_data(survey_sudo, answer_sudo, **post)

        if answer_sudo.state == 'done':
            survey_content = request.env['ir.qweb']._render('survey.survey_fill_form_done', survey_data)
        else:
            survey_content = request.env['ir.qweb']._render('survey.survey_fill_form_in_progress', survey_data)

        survey_progress = False
        if answer_sudo.state == 'in_progress' and not survey_data.get('question', request.env['survey.question']).is_page:
            if survey_sudo.questions_layout == 'page_per_section':
                page_ids = survey_sudo.page_ids.ids
                survey_progress = request.env['ir.qweb']._render('survey.survey_progression', {
                    'survey': survey_sudo,
                    'page_ids': page_ids,
                    'page_number': page_ids.index(survey_data['page'].id) + (1 if survey_sudo.progression_mode == 'number' else 0)
                })
            elif survey_sudo.questions_layout == 'page_per_question':
                page_ids = (answer_sudo.predefined_question_ids.ids
                            if not answer_sudo.is_session_answer and survey_sudo.questions_selection == 'random'
                            else survey_sudo.question_ids.ids)
                survey_progress = request.env['ir.qweb']._render('survey.survey_progression', {
                    'survey': survey_sudo,
                    'page_ids': page_ids,
                    'page_number': page_ids.index(survey_data['question'].id)
                })

        background_image_url = survey_sudo.background_image_url
        if 'question' in survey_data:
            background_image_url = survey_data['question'].background_image_url
        elif 'page' in survey_data:
            background_image_url = survey_data['page'].background_image_url

        return {
            'has_skipped_questions': any(answer_sudo._get_skipped_questions()),
            'survey_content': survey_content,
            'survey_progress': survey_progress,
            'survey_navigation': request.env['ir.qweb']._render('survey.survey_navigation', survey_data),
            'background_image_url': background_image_url
        }

    def _prepare_survey_data(self, survey_sudo, answer_sudo, **post):
        """ This method prepares all the data needed for template rendering, in function of the survey user input state.
            :param post:
                - previous_page_id : come from the breadcrumb or the back button and force the next questions to load
                                     to be the previous ones.
                - next_skipped_page : force the display of next skipped question or page if any."""
        data = {
            'is_html_empty': is_html_empty,
            'survey': survey_sudo,
            'answer': answer_sudo,
            'skipped_questions': answer_sudo._get_skipped_questions(),
            'breadcrumb_pages': [{
                'id': page.id,
                'title': page.title,
            } for page in survey_sudo.page_ids],
            'format_datetime': lambda dt: format_datetime(request.env, dt, dt_format=False),
            'format_date': lambda date: format_date(request.env, date)
        }
        if survey_sudo.questions_layout != 'page_per_question':
            triggering_answers_by_question, triggered_questions_by_answer, selected_answers = answer_sudo._get_conditional_values()
            data.update({
                'triggering_answers_by_question': {
                    question.id: triggering_answers.ids
                    for question, triggering_answers in triggering_answers_by_question.items() if triggering_answers
                },
                'triggered_questions_by_answer': {
                    answer.id: triggered_questions.ids
                    for answer, triggered_questions in triggered_questions_by_answer.items()
                },
                'selected_answers': selected_answers.ids
            })

        if not answer_sudo.is_session_answer and survey_sudo.is_time_limited and answer_sudo.start_datetime:
            data.update({
                'server_time': fields.Datetime.now(),
                'timer_start': answer_sudo.start_datetime.isoformat(),
                'time_limit_minutes': survey_sudo.time_limit
            })

        page_or_question_key = 'question' if survey_sudo.questions_layout == 'page_per_question' else 'page'

        # Bypass all if page_id is specified (comes from breadcrumb or previous button)
        if 'previous_page_id' in post:
            previous_page_or_question_id = int(post['previous_page_id'])
            new_previous_id = survey_sudo._get_next_page_or_question(answer_sudo, previous_page_or_question_id, go_back=True).id
            page_or_question = request.env['survey.question'].sudo().browse(previous_page_or_question_id)
            data.update({
                page_or_question_key: page_or_question,
                'previous_page_id': new_previous_id,
                'has_answered': answer_sudo.user_input_line_ids.filtered(lambda line: line.question_id.id == new_previous_id),
                'can_go_back': survey_sudo._can_go_back(answer_sudo, page_or_question),
            })
            return data

        if answer_sudo.state == 'in_progress':
            next_page_or_question = None
            if answer_sudo.is_session_answer:
                next_page_or_question = survey_sudo.session_question_id
            else:
                if 'next_skipped_page' in post:
                    next_page_or_question = answer_sudo._get_next_skipped_page_or_question()
                if not next_page_or_question:
                    next_page_or_question = survey_sudo._get_next_page_or_question(
                        answer_sudo,
                        answer_sudo.last_displayed_page_id.id if answer_sudo.last_displayed_page_id else 0)
                    # fallback to skipped page so that there is a next_page_or_question otherwise this should be a submit
                    if not next_page_or_question:
                        next_page_or_question = answer_sudo._get_next_skipped_page_or_question()

                if next_page_or_question:
                    if answer_sudo.survey_first_submitted:
                        survey_last = answer_sudo._is_last_skipped_page_or_question(next_page_or_question)
                    else:
                        survey_last = survey_sudo._is_last_page_or_question(answer_sudo, next_page_or_question)
                    data.update({'survey_last': survey_last})

            if answer_sudo.is_session_answer and next_page_or_question.is_time_limited:
                data.update({
                    'timer_start': survey_sudo.session_question_start_time.isoformat(),
                    'time_limit_minutes': next_page_or_question.time_limit / 60
                })

            data.update({
                page_or_question_key: next_page_or_question,
                'has_answered': answer_sudo.user_input_line_ids.filtered(lambda line: line.question_id == next_page_or_question),
                'can_go_back': survey_sudo._can_go_back(answer_sudo, next_page_or_question),
            })
            if survey_sudo.questions_layout != 'one_page':
                data.update({
                    'previous_page_id': survey_sudo._get_next_page_or_question(answer_sudo, next_page_or_question.id, go_back=True).id
                })
        elif answer_sudo.state == 'done' or answer_sudo.survey_time_limit_reached:
            # Display success message
            return self._prepare_survey_finished_values(survey_sudo, answer_sudo)

        return data

    def _prepare_survey_finished_values(self, survey, answer, token=False):
        values = {'survey': survey, 'answer': answer}
        if token:
            values['token'] = token
        return values

    @http.route('/survey/submit/<string:survey_token>/<string:answer_token>', type='json', auth='public', website=True)
    def survey_submit(self, survey_token, answer_token, **post):
        """ Submit a page from the survey.
        This will take into account the validation errors and store the answers to the questions.
        If the time limit is reached, errors will be skipped, answers will be ignored and
        survey state will be forced to 'done'.
        Also returns the correct answers if the scoring type is 'scoring_with_answers_after_page'."""
        # Survey Validation

        access_data = self._get_access_data(survey_token, answer_token, ensure_token=True)
        if access_data['validity_code'] is not True:
            return {}, {'error': access_data['validity_code']}
        survey_sudo, answer_sudo = access_data['survey_sudo'], access_data['answer_sudo']

        if answer_sudo.state == 'done':
            return {}, {'error': 'unauthorized'}

        questions, page_or_question_id = survey_sudo._get_survey_questions(answer=answer_sudo,
                                                                           page_id=post.get('page_id'),
                                                                           question_id=post.get('question_id'))

        if not answer_sudo.test_entry and not survey_sudo._has_attempts_left(answer_sudo.partner_id, answer_sudo.email, answer_sudo.invite_token):
            # prevent cheating with users creating multiple 'user_input' before their last attempt
            return {}, {'error': 'unauthorized'}

        if answer_sudo.survey_time_limit_reached or answer_sudo.question_time_limit_reached:
            if answer_sudo.question_time_limit_reached:
                time_limit = survey_sudo.session_question_start_time + relativedelta(
                    seconds=survey_sudo.session_question_id.time_limit
                )
                time_limit += timedelta(seconds=3)
            else:
                time_limit = answer_sudo.start_datetime + timedelta(minutes=survey_sudo.time_limit)
                time_limit += timedelta(seconds=10)
            if fields.Datetime.now() > time_limit:
                # prevent cheating with users blocking the JS timer and taking all their time to answer
                return {}, {'error': 'unauthorized'}

        errors = {}
        # Prepare answers / comment by question, validate and save answers
        for question in questions:
            inactive_questions = request.env['survey.question'] if answer_sudo.is_session_answer else answer_sudo._get_inactive_conditional_questions()
            if question in inactive_questions:  # if question is inactive, skip validation and save
                continue
            answer, comment = self._extract_comment_from_answers(question, post.get(str(question.id)))
            errors.update(question.validate_question(answer, comment))
            if not errors.get(question.id):
                answer_sudo._save_lines(question, answer, comment, overwrite_existing=survey_sudo.users_can_go_back or question.save_as_nickname or question.save_as_email)

        if errors and not (answer_sudo.survey_time_limit_reached or answer_sudo.question_time_limit_reached):
            return {}, {'error': 'validation', 'fields': errors}

        if not answer_sudo.is_session_answer:
            answer_sudo._clear_inactive_conditional_answers()

        # Get the page questions correct answers if scoring type is scoring after page
        correct_answers = {}
        if survey_sudo.scoring_type == 'scoring_with_answers_after_page':
            scorable_questions = (questions - answer_sudo._get_inactive_conditional_questions()).filtered('is_scored_question')
            correct_answers = scorable_questions._get_correct_answers()

        if answer_sudo.survey_time_limit_reached or survey_sudo.questions_layout == 'one_page':
            answer_sudo._mark_done()
        elif 'previous_page_id' in post:
            # when going back, save the last displayed to reload the survey where the user left it.
            answer_sudo.last_displayed_page_id = post['previous_page_id']
            # Go back to specific page using the breadcrumb. Lines are saved and survey continues
            return correct_answers, self._prepare_question_html(survey_sudo, answer_sudo, **post)
        elif 'next_skipped_page_or_question' in post:
            answer_sudo.last_displayed_page_id = page_or_question_id
            return correct_answers, self._prepare_question_html(survey_sudo, answer_sudo, next_skipped_page=True)
        else:
            if not answer_sudo.is_session_answer:
                page_or_question = request.env['survey.question'].sudo().browse(page_or_question_id)
                if answer_sudo.survey_first_submitted and answer_sudo._is_last_skipped_page_or_question(page_or_question):
                    next_page = request.env['survey.question']
                else:
                    next_page = survey_sudo._get_next_page_or_question(answer_sudo, page_or_question_id)
                if not next_page:
                    if survey_sudo.users_can_go_back and answer_sudo.user_input_line_ids.filtered(
                            lambda a: a.skipped and a.question_id.constr_mandatory):
                        answer_sudo.write({
                            'last_displayed_page_id': page_or_question_id,
                            'survey_first_submitted': True,
                        })
                        return correct_answers, self._prepare_question_html(survey_sudo, answer_sudo, next_skipped_page=True)
                    else:
                        answer_sudo._mark_done()

            answer_sudo.last_displayed_page_id = page_or_question_id
        ticket_comment=post.get('ticket_comment')
        self.get_user_input_lines(answer_sudo,survey_sudo,ticket_comment)
        return correct_answers, self._prepare_question_html(survey_sudo, answer_sudo)

    def get_user_input_lines(self, answer_sudo,survey_sudo,ticket_comment):
        answer_question_split = request.env["survey.user_input.line"].search_read([("id", "in", answer_sudo.read()[0]["user_input_line_ids"])])
        for answer in answer_question_split:
            answer_question_id = answer["question_id"][0]
            answer_question_value = answer["display_name"]
            if answer["suggested_answer_id"] :
                suggested_answer_id=int(answer["suggested_answer_id"][0])
            else :
                suggested_answer_id =False
            survey_question_id = request.env["survey.question"].search([("id", "=", int(answer_question_id))])
            chosen_answer = survey_question_id.suggested_answer_ids.filtered(lambda x: x.value == answer_question_value)
            self.create_ticket(chosen_answer,survey_sudo,survey_question_id,ticket_comment,suggested_answer_id)

    def create_ticket(self,chosen_answer,survey_sudo,survey_question_id,ticket_comment,suggested_answer_id):
        if chosen_answer.create_ticket:
            if not self.check_ticket_existing(survey_sudo,survey_question_id,suggested_answer_id):
                request.env["helpdesk.ticket"].create(
                    {"name": survey_question_id.title, "team_id": survey_sudo.helpdesk_team_id.id,"suggested_answer_id": suggested_answer_id,
                     "description": ticket_comment})

    def check_ticket_existing(self,survey_sudo,survey_question_id,suggested_answer_id):
        ticket_id = request.env["helpdesk.ticket"].search(
            [("name", "=", survey_question_id.title),
             ("team_id", "=", survey_sudo.helpdesk_team_id.id),
             ("suggested_answer_id", "=", suggested_answer_id)])
        return bool(ticket_id)



