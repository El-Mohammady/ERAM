/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { _t } from "@web/core/l10n/translation";
import { rpc } from "@web/core/network/rpc";

publicWidget.registry.SurveyFormWidget.include({
    start: async function () {
        await this._super.apply(this, arguments);
    },

    /**
     * Override an existing method (_onSubmit).
    */
    _submitForm: async function (options) {
        var params = {};
        if (options.previousPageId) {
            params.previous_page_id = options.previousPageId;
        }
        if (options.nextSkipped) {
            params.next_skipped_page_or_question = true;
        }
        var route = "/survey/submit";

        if (this.options.isStartScreen) {
            route = "/survey/begin";
            // Hide survey title in 'page_per_question' layout: it takes too much space
            if (this.options.questionsLayout === 'page_per_question') {
                this.$('.o_survey_main_title').fadeOut(400);
            }
        } else {
            var $form = this.$('form');
            var formData = new FormData($form[0]);

            if (!options.skipValidation) {
                // Validation pre submit
                if (!this._validateForm($form, formData)) {
                    return;
                }
            }

            this._prepareSubmitValues(formData, params);
        }

        // prevent user from submitting more times using enter key
        this.preventEnterSubmit = true;

        if (this.options.sessionInProgress) {
            // reset the fadeInOutDelay when attendee is submitting form
            this.fadeInOutDelay = 400;
            // prevent user from clicking on matrix options when form is submitted
            this.readonly = true;
        }
        var final_comment = "";
        self.$('input[name="ticket_comment"]').each(function() {
            if ($(this).val()){
                final_comment = $(this).val();
            }
        });
        params["ticket_comment"]=final_comment
        const submitPromise = rpc(
            `${route}/${this.options.surveyToken}/${this.options.answerToken}`,
            params
        );
        if (!this.options.isStartScreen && this.options.scoringType == 'scoring_with_answers_after_page') {
            const [correctAnswers] = await submitPromise;
            if (Object.keys(correctAnswers).length && document.querySelector('.js_question-wrapper')) {
                this._showCorrectAnswers(correctAnswers, submitPromise, options);
                return;
            }
        }
        this._nextScreen(submitPromise, options);
    },
});
