//called in <Card>, an mdl title card that just renders the title text.
var TitleSection = React.createClass({
    render: function(){
      return (
        <div className="mdl-card__title mdl-card--expand mdl-color--primary">
          <h2 className="mdl-card__title-text white_text"> { this.props.titleText } </h2>
        </div>
      );
    }
});

var TitleSurvey = React.createClass({
    render: function(){
      return (
        <div className="mdl-card__title mdl-card--expand mdl-color--primary">
          <h1 className="mdl-card__title-text white_text"> { this.props.title } </h1>
        </div>
      );
    }
});

var Card = React.createClass({
    /*Since our children are dynamic the mdl needs to be reprocessed after every render else it looks like regular html, so everytime Card updates
    with new props (which happens every time next or previous is clicked) we upgrade all our components to mdl again*/
    multipleChoiceResponseState: function(){
        var length = Object.keys(this.props.options).length;
        var questionObj = [];
        var responseState = this.props.responseState;
        var responseStateLength = Object.keys(responseState).length;
        var prevAnswers = [];

        for(var i =0; i < length; i++){
            questionObj[i] = 0;
        }

        for(var i = responseStateLength-1; i >= 0; i--){
          if(responseState[i].question_id == this.props.questionID){
             prevAnswers = responseState[i].response_data;
             for(var i2 =0; i2 < length; i2++){
                 if(prevAnswers[i2] == 1){
                    questionObj[i2]= 1;
                 }
             }
          }
        }
        return questionObj;
    },

    singleChoiceResponseState: function(){
        var length = Object.keys(this.props.options).length;
        var questionObj =[];
        var responseState = this.props.responseState;
        var responseStateLength = Object.keys(responseState).length;
        var prevAnswers = [];
        for(var i =0; i < length; i++){
            questionObj[i]=0;
        }
        for(var i = responseStateLength-1; i >= 0; i--){
            if(responseState[i].question_id == this.props.questionID){
                prevAnswers = responseState[i].response_data;
                    for(var i2 = 0; i2 < length; i2++){
                        if(prevAnswers[i2]==1){
                            questionObj[i2] = 1;
                        }
                    }
            }
        }
        return questionObj;
    },

    freeResponseResponseState: function(){
        var responseState = this.props.responseState;
        var responseStateLength = Object.keys(responseState).length;
        var prevAnswer = "Change Me!";
        for(var i = responseStateLength-1; i >= 0; i--){
          if(responseState[i].question_id == this.props.questionID){
             prevAnswer = responseState[i].response_data;
          }
        }
        return prevAnswer;
    },

    ratingResponseState: function(){
		var responseState = this.props.responseState;
        var responseStateLength = Object.keys(responseState).length;
        var prevAnswer = 5;
        for(var i = responseStateLength-1; i >= 0; i--){
          if(responseState[i].question_id == this.props.questionID){
             prevAnswer = responseState[i].response_data;
          }
        }
        return prevAnswer;
	},


    /* Our children are dynamic so I wanted to make sure we're including keys where we can, questionID's are unique and by adding .card we'll ensure
    they're unique from further children down the line, otherwise this layer just looks to generate the correct type of question card based off of
    this.props.response_format as well as a <TitleSection> component which is passed this.props.title*/
    render: function(){
        var cardType = "";
        var key = String(this.props.questionID) + "." + "card";
        if(this.props.response_format == "multipleChoice"){
        cardType = <MultipleChoice key={key} questionState={this.multipleChoiceResponseState()} {...this.props}/>
        } else if(this.props.response_format == "rating"){
            cardType = <Rating key={key} questionState={this.ratingResponseState()} {...this.props}/>
        } else if (this.props.response_format == "trueOrFalse"){
            cardType = <SingleChoice key={key} questionState={this.singleChoiceResponseState()} {...this.props}/>
        } else if (this.props.response_format == "freeResponse"){
            cardType = <FreeResponse key={key} questionState={this.freeResponseResponseState()} {...this.props}/>
        } else {
            console.log("not Valid card type");
            return undefined;
        }
        return (
            <div className="updates mdl-card mdl-shadow--2dp mdl-cell mdl-cell--4-col mdl-cell--8-col-tablet mdl-cell--12-col-desktop">
                <div>
                <TitleSurvey title={this.props.surveyTitle}/>
                <TitleSection titleText={this.props.title}/>
                    {cardType}
                </div>
            </div>
        );
    }
});
