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

    loadPageJSON: function() {
    $.ajax({
    url:this.props.routes.surveys,
    type: 'GET',
    dataType: 'json',
    cache: false,
    success: function(data){
    this.setState({data: data});
    }.bind(this)
    });
    },
    
    handleSurveySubmit: function(survey){
    $.ajax({
    url: this.props.routes.surveys,
    dataType: 'json'.
    type: 'POST',
    data: survey,
    success: function(data){
    }.bind(this)
    error: function(xhr, status,err){
    console.error(this.props.url.surveys, status, err.toString());
    }.bind(this)
    });
    },
    
    getInitialState: function() {
    return{data:[]};
    },
    
    componentDidMount: function(){
        this.loadPageJSON()
    },
    
    render: function(){
      return (
        <div className="mdl-grid mdl-cell--12-col content">
            <MainDiv pageJson={this.state.data} />
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
