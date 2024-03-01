document.addEventListener("DOMContentLoaded", function() {
    var buttons = document.querySelectorAll('.buttons button');
    var contents = document.querySelectorAll('.content');

    buttons.forEach(function(btn) {
        btn.addEventListener('click', function() {
            var contentId = this.id.replace('btn', '');
            var content = document.getElementById(contentId);

            contents.forEach(function(el) {
                el.style.display = 'none';
            });
            content.style.display = 'block';
        });
    });
});