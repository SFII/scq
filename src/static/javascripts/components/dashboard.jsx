var testQuestions = [
{
    id : 1,
    type : "trueOrFalse",
    title :"Would you recommend this course?",
    options : ["Yes", "No"]
},
{
    id : "asdasdad",
    type : "freeResponse",
    title :"What things should be improved?"
},
{
    id : 2,
    type : "multipeChoice",
    title: "Did you enjoy the course?",
    options: ["Not at all","It was an average course","It was an excellent course"]
}
];

/*
*
* MainDiv
*ask michael about this.props.class
*/
var MainDiv = React.createClass({
    render: function() {
        var itemNodes = testQuestions.map(function (item) {
                return (
                    <Card title={item.title} options={item.options} type={item.type}>
                    </Card>
                );
            });
        return (
        <div className="mainDiv ">
            {itemNodes}
        </div>
        );
    }
});

var Page = React.createClass({
    render: function(){
      return (
        <div className="mdl-grid mdl-cell--12-col content">
            <MainDiv question={this.props.question}/>
        </div>
        );
    }
});

/*
*
* Form
*
*/
var Form = React.createClass({

    addItem: function(e) {
        e.preventDefault();
        this.props.onItemSubmit({});
        return;

    },

    render: function() {
        return (
        <form className="listForm" onSubmit={this.addItem}>
        <input  type="submit" value="Click me" />
        </form>
        );
    }
});