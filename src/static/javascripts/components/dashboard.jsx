var testQuestions = [
    {
        surveyID: "Unique-ID",
        department:"",
        creator:"",
        isInstructor:"",
        questions : [
            {
                id: 1,
                type: "trueOrFalse",
                title: "Would you recommend this course?",
                options: ["Yes", "No"]
            }, {
                id: "asdasdad",
                type: "freeResponse",
                title: "What things should be improved?"
            }, {
                id: 2,
                type: "multipeChoice",
                title: "Did you enjoy the course?",
                options: ["Not at all", "It was an average course", "It was an excellent course"]
            }
        ]
    },
    
    {
        surveyID: "Unique-ID",
        department:"",
        creator:"",
        isInstructor:"",
        questions : [
            {
                id: "asdasdad",
                type: "freeResponse",
                title: "What did you not like about the course?"
            }, {
                id: 1,
                type: "trueOrFalse",
                title: "Will you take another course in the same field?",
                options: ["Yes", "No"]
            }, {
                id: 2,
                type: "trueOrFalse",
                title: "Was the grade policy fair?",
                options: ["Yes", "No"]
            }
        ]
    },
    
    {
        surveyID: "Unique-ID",
        department:"",
        creator:"",
        isInstructor:"",
        questions : [
            {
                id: 1,
                type: "trueOrFalse",
                title: "Would you recommend this course?",
                options: ["Yes", "No"]
            }, {
                id: "asdasdad",
                type: "freeResponse",
                title: "What things should be improved?"
            }, {
                id: 2,
                type: "multipeChoice",
                title: "Did you enjoy the course?",
                options: ["Not at all", "It was an average course", "It was an excellent course"]
            }
        ]
    }
];

var Page = React.createClass({

    loadPageJSON: function() {
    $.ajax({
    url:this.props.routes.surveys,
    type: 'GET',
    dataType: 'json',
    cache: true,
    success: function(data){
    this.setState({data: data});
    }.bind(this),
    error: function(xhr, status, err){
        console.error(this.props.routes.surveys, status, err.toString());
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
* MainDiv
*ask michael about this.props.class
*/
var MainDiv = React.createClass({
    render: function() {
		if (!loggedIn()) {
		   return (<Welcome />);
		}
        var itemNodes = this.props.pageJson.map(function (item) {
                return (
                    <SurveyDiv 
                    questions={item.questions}>
                    </SurveyDiv>
                );
            });
        return (
        <div className="mainDiv ">
            {itemNodes}
        </div>
        );
    }
});
    
var SurveyDiv = React.createClass({
    render: function() {
        var itemSurvey = this.props.questions.map(function (itemSurvey) {  
            return(
                <Card
                title={itemSurvey.title}
                options={itemSurvey.options}
                type={itemSurvey.type}>
                </Card>
            );
        });
        return(
        <div className="surveyDiv">
            {itemSurvey}
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
