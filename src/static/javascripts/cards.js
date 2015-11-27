// var MediumCard = React.createClass({
//
//     propTypes: {
//         survey: React.PropTypes.object.isRequired
//     },
//
//    render: function(){
//       return(
//          <div className="updates mdl-card mdl-shadow--2dp mdl-cell mdl-cell--8-col">
//             <Card survey={ this.props.survey }/>
//          </div>
//       );
//    }
// });
//
// var SmallCard = React.createClass({
//    render: function(){
//       return(
//          <div className="updates mdl-card mdl-shadow--2dp mdl-cell mdl-cell--4-col">
//             <Card options={ ['Small', 'TEST', 'SAMPLE THREE']}/>
//          </div>
//       );
//    }
// });
//
// var BigCard = React.createClass({
//     render: function() {
//         return (
//             <div className="updates mdl-card mdl-shadow--2dp mdl-cell mdl-cell--4-col mdl-cell--8-col-tablet mdl-cell--12-col-desktop">
//             <Card options={ ['SAMPLE ONE', 'SAMPLE TWO', 'SAMPLE THREE'] }/>
//         </div>
//         );
//     }
// });
// var SupportSection = React.createClass({
//
//     render: function(){
//       return (
//         <div className="mdl-card__supporting-text mdl-color-text--grey-600">
//             { this.props.survey }
//         </div>
//       );
//     }
// });

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
      if(this.props.type=="multipeChoice"){
        return (
          <div className="updates mdl-card mdl-shadow--2dp mdl-cell mdl-cell--4-col mdl-cell--8-col-tablet mdl-cell--12-col-desktop">
            <div>
              <TitleSection titleText={this.props.title}/>
              <MultipleChoice options={this.props.options}/>
            </div>
          </div>
        );
      } else if (this.props.type=="trueOrFalse"){
          return (
            <div className="updates mdl-card mdl-shadow--2dp mdl-cell mdl-cell--4-col mdl-cell--8-col-tablet mdl-cell--12-col-desktop">
              <div>
                <TitleSection titleText={this.props.title}/>
                <SingleChoice options={this.props.options} />
              </div>
            </div>
          );
    } else if (this.props.type=="freeResponse"){
        return (
          <div className="updates mdl-card mdl-shadow--2dp mdl-cell mdl-cell--4-col mdl-cell--8-col-tablet mdl-cell--12-col-desktop">
            <div>
            <TitleSection titleText={this.props.title}/>
            <FreeResponse/>
            </div>
        </div>
      );
    } else {
        alert("not Valid card type");
        return undefined;;
    }
  }
});


