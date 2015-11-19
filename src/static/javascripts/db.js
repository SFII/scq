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

function postAnswer(){

}

getQuestion(){
    return
        {
        "question-id" : "Unique-ID",
        "type" : "multipleChoice",
        "question":"Did you enjoy the course?",
        "options":["Not at all","It was an average course","It was an excellent course"],
        }
}

renderQuestion(question_object){
    if question_object.type == "trueOrFalse" {
        render
    }
}

renderQuestion(getQuestion())