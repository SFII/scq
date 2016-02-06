var TitleSection = React.createClass({
    render: function(){
      return (
        <div className="mdl-card__title mdl-card--expand mdl-color--teal-300">
          <h2 className="mdl-card__title-text"> { this.props.titleText } </h2>
        </div>
      );
    }
});
//Card is really messy
var Card = React.createClass({
    /* an initial state called response, actually not entirely sure
     * why we have it.. :) 
    */
    getInitialState: function(){
        return {response: []};
    },
    
    //handleSurveySubmit is called whenever a submit button is pushed
    //it calls POST on /api/response sending a JSON of the survey data
    //and on success calls the removeHandler which removes the 
    //corresponding cards 
    handleSurveySubmit: function(survey){
        console.log(survey);
        $.ajax({
            url: this.props.routes.response,
			contentType: 'application/json',
            type: 'POST',
            data: JSON.stringify(survey),
            success: function(data){
                console.log("Post success");
                this.props.removeHandler();
            }.bind(this),
			error: function(xhr, status,err){
				console.error("/api/response", status, err.toString());
			}.bind(this)
        });
    },
    //case matching of the question type, generates the corresponding
    //card, eventually we want one card per survey, this will be tricky
    render: function(){
      if(this.props.response_format == "multipleChoice"){
        return (
          <div className="updates mdl-card mdl-shadow--2dp mdl-cell mdl-cell--4-col mdl-cell--8-col-tablet mdl-cell--12-col-desktop">
            <div>
              <TitleSection titleText={this.props.title}/>
              <MultipleChoice 
              options={this.props.options}
              onSubmit={this.handleSurveySubmit}
              surveyID={this.props.surveyID}
              department={this.props.department}
              creator={this.props.creator}
              isInstructor={this.props.isInstructor}/>
            </div>
          </div>
        );
      }else if(this.props.response_format == "rating"){
        return (
          <div className="updates mdl-card mdl-shadow--2dp mdl-cell mdl-cell--4-col mdl-cell--8-col-tablet mdl-cell--12-col-desktop">
            <div>
              <TitleSection titleText={this.props.title}/>
              <Rating 
              surveyID={this.props.surveyID}
              department={this.props.department}
              creator={this.props.creator}
              isInstructor={this.props.isInstructor}/>
            </div>
          </div>
        );
       }else if (this.props.response_format == "trueOrFalse"){
          return (
            <div className="updates mdl-card mdl-shadow--2dp mdl-cell mdl-cell--4-col mdl-cell--8-col-tablet mdl-cell--12-col-desktop">
              <div>
                  <TitleSection titleText={this.props.title}/>
                  <SingleChoice 
                  options={this.props.options}
                  onSubmit={this.handleSurveySubmit}
                  surveyID={this.props.surveyID}
                  department={this.props.department}
                  creator={this.props.creator}
                  isInstructor={this.props.isInstructor}/>
              </div>
            </div>
          );
    } else if (this.props.response_format == "freeResponse"){
        return (
          <div className="updates mdl-card mdl-shadow--2dp mdl-cell mdl-cell--4-col mdl-cell--8-col-tablet mdl-cell--12-col-desktop">
            <div>
              <TitleSection titleText={this.props.title}/>
              <FreeResponse 
              onSubmit={this.handleSurveySubmit}
              surveyID={this.props.surveyID}
              department={this.props.department}
              creator={this.props.creator}
              isInstructor={this.props.isInstructor}/>
            </div>
        </div>
      );
    } else {
        alert("not Valid card type");
        return undefined;;
    }
  }
});