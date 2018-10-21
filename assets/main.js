var input = document.getElementById('images');
var label = input.nextElementSibling,
labelVal = label.innerHTML;

input.addEventListener( 'change', function( e )
{
    var fileName = '';

    console.log(this);
    if (this.files && this.files.length > 1)
        fileName = (this.getAttribute('data-multiple-caption') || '').replace('{count}', this.files.length);
    else
        fileName = e.target.value.split('\\').pop();

    if (fileName)
        label.querySelector('div').innerHTML = fileName;
    else
        label.innerHTML = labelVal;
});
