(function ($) {
    var pub = yii.validation;
    pub.multiRequired = function(value, messages, options){
        var valid = false;
        $(options.compareAttribute).each(function(i, attr){
            var compareValue = $('#' + attr).val(),
                isString = typeof compareValue == 'string' || compareValue instanceof String;
            
            valid |= !pub.isEmpty(isString ? $.trim(compareValue) : compareValue);
        });
    
        if (!valid) {
            pub.addMessage(messages, options.message, value);
        }
        // window.thisform = this;
        console.log(options);
    };
})(jQuery);