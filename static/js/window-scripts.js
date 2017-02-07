var toogle = 0;

function toogleFrame()
{
    if (toogle == 0)
    {
        document.getElementById('windowFrame').style.height = '45px';
        toogle = 1;
    }
    else
    {
        document.getElementById('windowFrame').style.height = '510px';
        toogle = 0; 
    }
}