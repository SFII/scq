//called in <Card>, an mdl title card that just renders the title text.
var TitleSection = React.createClass({
    render: function(){
      return (
        <div className="mdl-card__title mdl-card--expand mdl-color--primary">
          <h2 className="mdl-card__title-text"> { this.props.titleText } </h2>
        </div>
      );
    }
});

var Card = React.createClass({
    /*Since our children are dynamic the mdl needs to be reprocessed after every render else it looks like regular html, so everytime Card updates
    with new props (which happens every time next or previous is clicked) we upgrade all our components to mdl again*/
    componentDidUpdate: function(){
        componentHandler.upgradeDom();
    },
    
    /* Our children are dynamic so I wanted to make sure we're including keys where we can, questionID's are unique and by adding .card we'll ensure
    they're unique from further children down the line, otherwise this layer just looks to generate the correct type of question card based off of 
    this.props.response_format as well as a <TitleSection> component which is passed this.props.title*/
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
