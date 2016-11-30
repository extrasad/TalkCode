var LetterCounter = function(min=1, max, field, button, counter_text) {
  field.keyup(function() {

      this.min = min;
      this.max = max;

        var postLength = $(this).val().length;
        var charactersLeft = this.max - postLength;
        counter_text.text(charactersLeft);

        if(charactersLeft < this.min) {
          button.addClass('disabled').prop("disabled", true);
        }
        else if(charactersLeft == this.max) {
          button.addClass('disabled').prop("disabled", true);
        }
        else {
          button.removeClass('disabled').prop("disabled", false);
        }
      });

      button.addClass('disabled').prop("disabled", true);
}
