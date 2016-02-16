function getSurvey(url){
    $.ajax({
     url: url,
     type: 'GET',
     async: false,
     cache: false,
     timeout: 30000,
     error: function(){
         return {};
     },
     success: function(data){
         console.log(data)
         return data;
     }
    });
}

function sendSurvey(url){
}