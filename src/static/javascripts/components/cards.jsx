var TitleSection = React.createClass({
    render: function(){
      return (
        <div className="mdl-card__title mdl-card--expand mdl-color--teal-300">
          <h2 className="mdl-card__title-text"> { this.props.titleText } </h2>
        </div>
      );
    }
});

var Card = React.createClass({
    
    getInitialState: function(){
        return {response: []};
    },
    
    handleSurveySubmit: function(survey){
        console.log(survey);
        $.ajax({
            url: "/api/response",
            dataType: 'json',
            type: 'POST',
            data: survey,
            success: function(data){
        }.bind(this),
        error: function(xhr, status,err){
            console.error("/api/response", status, err.toString());
        }.bind(this)
        });
    },
    
    render: function(){
      if(this.props.type == "multipeChoice"){
        return (
          <div className="updates mdl-card mdl-shadow--2dp mdl-cell mdl-cell--4-col mdl-cell--8-col-tablet mdl-cell--12-col-desktop">
            <div>
              <TitleSection titleText={this.state.response}/>
              <MultipleChoice options={this.props.options} onSubmit={this.handleSurveySubmit}/>
            </div>
          </div>
        );
      }else if(this.props.type == "rating"){
        return (
          <div className="updates mdl-card mdl-shadow--2dp mdl-cell mdl-cell--4-col mdl-cell--8-col-tablet mdl-cell--12-col-desktop">
            <div>
              <TitleSection titleText={this.props.title}/>
              <Rating />
            </div>
          </div>
        );
       }else if (this.props.type == "trueOrFalse"){
          return (
            <div className="updates mdl-card mdl-shadow--2dp mdl-cell mdl-cell--4-col mdl-cell--8-col-tablet mdl-cell--12-col-desktop">
              <div>
                  <TitleSection titleText={this.props.title}/>
                  <SingleChoice options={this.props.options} onSubmit={this.handleSurveySubmit} />
              </div>
            </div>
          );
    } else if (this.props.type == "freeResponse"){
        return (
          <div className="updates mdl-card mdl-shadow--2dp mdl-cell mdl-cell--4-col mdl-cell--8-col-tablet mdl-cell--12-col-desktop">
            <div>
              <TitleSection titleText={this.props.title}/>
              <FreeResponse onSubmit={this.handleSurveySubmit}/>
            </div>
        </div>
      );
    } else {
        alert("not Valid card type");
        return undefined;;
    }
  }
});
