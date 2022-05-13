(function($) {
    $(document).ready(function($) {
        document.getElementById("set_discount-group").style.display = "none";
        document.getElementById("basket_discount-group").style.display = "none";
        $("select[name='discount_type']").change(function() {
            document.getElementById("product_discount-group").style.display = "none";
            document.getElementById("set_discount-group").style.display = "none";
            document.getElementById("basket_discount-group").style.display = "none";
            var selectValue = $("select[name='discount_type']").val();
            if (selectValue == "PD") {
                document.getElementById("product_discount-group").removeAttribute('style');
            };
            if (selectValue == "SD") {
                document.getElementById("set_discount-group").removeAttribute('style');
            };
            if (selectValue == "BD") {
                document.getElementById("basket_discount-group").removeAttribute('style');
            };
        }); 
    });
})(django.jQuery);
