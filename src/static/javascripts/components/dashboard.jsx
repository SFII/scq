var testQuestions = [
{
    id : 1,
    type : "trueOrFalse",
    title :"Would you recommend this course?",
    options : ["yes", "No"]
},
{
    id : "asdasdad",
    type : "freeResponse",
    title :"What things should be improved?"
},
{
    id : 2,
    type : "rating",
    title: "Please rate the course.",
    options : ["rate"]
}
];




/*
*
* MainDiv
*ask michael about this.props.class
*/
var MainDiv = React.createClass({
    render: function() {
		if (!loggedIn()) {
		   return (<Welcome />);
		}
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

function loggedIn() {
	return document.cookie.indexOf("user") > -1
}
