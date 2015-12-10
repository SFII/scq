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
    render: function(){
      if(this.props.type == "multipeChoice"){
        return (
          <div className="updates mdl-card mdl-shadow--2dp mdl-cell mdl-cell--4-col mdl-cell--8-col-tablet mdl-cell--12-col-desktop">
            <div>
              <TitleSection titleText={this.props.title}/>
              <MultipleChoice options={this.props.options}/>
            </div>
          </div>
        );
      }else if(this.props.type == "rating"){
        return (
          <div className="updates mdl-card mdl-shadow--2dp mdl-cell mdl-cell--4-col mdl-cell--8-col-tablet mdl-cell--12-col-desktop">
            <div>
              <TitleSection titleText={this.props.title}/>
              <Rating options={this.props.options}/>
            </div>
          </div>
        );
       }else if (this.props.type == "trueOrFalse"){
          return (
            <div className="updates mdl-card mdl-shadow--2dp mdl-cell mdl-cell--4-col mdl-cell--8-col-tablet mdl-cell--12-col-desktop">
              <div>
                  <TitleSection titleText={this.props.title}/>
                  <SingleChoice options={this.props.options} />
              </div>
            </div>
          );
    } else if (this.props.type == "freeResponse"){
        return (
          <div className="updates mdl-card mdl-shadow--2dp mdl-cell mdl-cell--4-col mdl-cell--8-col-tablet mdl-cell--12-col-desktop">
            <div>
              <TitleSection titleText={this.props.title}/>
              <FreeResponse />
            </div>
        </div>
      );
    } else {
        alert("not Valid card type");
        return undefined;;
    }
  }
});
