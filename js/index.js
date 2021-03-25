$(function () {
    url = $("#cajDown").attr("href");
    if(url){
        newurl = url.replace("dflag=cajdown", "dflag=pdfdown").replace("dflag=nhdown", "dflag=pdfdown");
        $("#cajDown").attr("href", newurl);
    }
    listurl = $(".downloadlink").attr("href");
    console.log(listurl);
    // if(listurl){
        $(".downloadlink").attr("href", listurl + "&dflag=pdfdown");
    // }
});