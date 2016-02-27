var TitleSection = React.createClass({
    render: function(){
      return (
        <div className="mdl-card__title mdl-card--expand mdl-color--primary">
          <h2 className="mdl-card__title-text"> { this.props.titleText } </h2>
        </div>
      );
    }
});

// Card confuses responses of the same type.
var Card = React.createClass({
    componentDidUpdate: function(){
        componentHandler.upgradeDom();
    },

    //handleSurveySubmit is called whenever a submit button is pushed
    //it calls POST on /api/response sending a JSON of the survey data
    //and on success calls the removeHandler which removes the
    //corresponding cards
    //case matching of the question type, generates the corresponding
    //card, eventually we want one card per survey, this will be tricky
    render: function(){
        var cardType = "";
        var key = String(this.props.questionID) + "." + "card"; 
        if(this.props.response_format == "multipleChoice"){
            cardType = <MultipleChoice key={key} {...this.props}/>
        } else if(this.props.response_format == "rating"){
            cardType = <Rating key={key} {...this.props}/>
        } else if (this.props.response_format == "trueOrFalse"){
            cardType = <SingleChoice key={key} {...this.props}/>
        } else if (this.props.response_format == "freeResponse"){
            cardType = <FreeResponse key={key} {...this.props}/>
        } else {
            console.log("not Valid card type");
            return undefined;
        }
        return (
            <div className="updates mdl-card mdl-shadow--2dp mdl-cell mdl-cell--4-col mdl-cell--8-col-tablet mdl-cell--12-col-desktop">
                <div>
                    <TitleSection titleText={this.props.title}/>
                    {cardType}
                </div>
            </div>
        );
    }
});
