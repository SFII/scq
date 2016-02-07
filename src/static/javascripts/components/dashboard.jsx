/*
* Page is the overall container that gets mounted into our HTML file
*/
var Page = React.createClass({
/*
//loadPageJSON is the function we call whenever we want to call GET on the surveys endpoint
    loadPageJSON: function() {
    $.ajax({
    url: this.props.routes.surveys,
    type: 'GET',
    dataType: 'json',
    cache: true,
    success: function(data){
    //on success we set the state of Page to be equal to the JSON received
    this.setState({data: data});
    }.bind(this),
    error: function(xhr, status, err){
        console.error(this.props.routes.surveys, status, err.toString());
    }.bind(this)
    });
    },
    //This is where the initial loadPageJSON call happens, it happens when the React class is instantiated (Carlos we should put that
    //initial fetch Sam showed you here)
    getInitialState: function() {
    //this.loadPageJSON();
        return{data:[]};
    },

    //This is something we'll likely want to change, it calls loadPageJSON again once the component mounts, which doesn't really make sense, oops

    //MainDiv is sent the data state as "pageJson" and the api routes json as "routes"
    */

    render: function(){
      return (
        <div className="mdl-grid mdl-cell--12-col content">
        <MainDiv /*pageJson={this.state.data}*/ routes={this.props.routes}/>
        </div>
      );
    }
});

/*
*
* MainDiv
* At this layer we separate each Survey into separate SurveyDiv objects
*/
var MainDiv = React.createClass({
    render: function() {
		if (!loggedIn()) {
		   return (<Welcome />);
		}
        routesObject=this.props.routes;
        //itemNodes is the set of mapped items (each one is a survey) and each is passed it's set of questions, routes, and other relevant information
        /*this is set to testQuestions.map until the GET works, if it's
        working switch it to this.props.pageJson and it should work */
        var itemNodes = data.map(function (item) {
                return (
                <SurveyDiv
                questions={item.questions}
                routes={routesObject}
                surveyID={item.surveyID}
                department={item.department}
                creator={item.creator}
                isInstructor={item.isInstructor}/>
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
    //We want our Survey cards to disappear once submitted, so the getInitialState and removeCard functions provide a boolean
    //that we check before/while rendering
    getInitialState: function() {
    return({
            length: Object.keys(this.props.questions).length,
            showCard: true,
            iter: 0,
            response: {
                survey_id: this.props.surveyID,
                question_responses:[]
            },
            
            });
    },  
    
    handleSurveySubmit: function(survey){
        console.log(survey);
        var response = this.state.response
        response.question_responses.push(JSON.stringify(survey));
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
    
    removeCard: function() {
        if(iter == 0){
            return;
        }
        this.setState({showCard: false});
    },

    nextQuestion: function(survey){
        console.log("nextQuestion");
        var response = this.state.response;
        response.question_responses.push(JSON.stringify(survey));
        console.log(response);
        var iter = this.state.iter;
        if(iter == this.state.length){
        }
        else{
            this.setState({iter: iter + 1});
        }
    },

    prevQuestion: function(survey){
        console.log("prevQuestion");
        var response = this.state.response;
        response.question_responses.push(JSON.stringify(survey));
        var iter = this.state.iter;
        if(iter == 0){
        }
        else{
            this.setState({iter: iter - 1});
        }
    },

    render: function() {
        //increasing the scope of the props, there has to be a better way to do this.
        //if showCard state is true, then we map the surveys questions onto cards, else we map nothing, pass all properties again.
        if(this.state.showCard == true) {
            return(
            <div className="surveyDiv">
                <Card
                routes={this.props.routes}
                questionNum={this.state.iter}
                questionID = {this.props.questions[this.state.iter].id}
                title={this.props.questions[this.state.iter].title}
                options={this.props.questions[this.state.iter].options}
                response_format={this.props.questions[this.state.iter].response_format}
                surveyID={this.props.surveyID}
                department={this.props.department}
                creator={this.props.creator}
                isInstructor={this.props.isInstructor}
                removeHandler={this.removeCard}
                nextHandler={this.nextQuestion}
                prevHandler={this.prevQuestion}
                onSubmit={this.handleSurveySubmit}>
                </Card>
            </div>
            );
        }
        else{
        }
    }
    });


function loggedIn() {
	return document.cookie.indexOf("user") > -1
}
