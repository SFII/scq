var HelpPage = React.createClass({

    render: function(){
        return(
            <div className="helpPageDiv mdl-cell mdl-cell--12-col">
                <GroupsHelp />
                <SurveysHelp />
                <Censorship />
                <InformationCollection />
            </div>
        );
    }
});

var GroupsHelp = React.createClass({
    
    getInitialState: function(){
        return({
            expanded: "false"
        });
    },
    
    expand: function(){
        this.setState({
            expanded: "true"
        });
    },
    
    contract: function(){
        this.setState({
            expanded: "false"
        });
    },
    
    render: function(){
    if(this.state.expanded == "true"){
        return(
          <div className="mdl-card mdl-shadow--2dp mdl-cell mdl-cell--12-col">
            <div className="mdl-card__title mdl-color--primary">
                <div className="mdl-cell mdl-cell--6-col">
                    <h2 className="mdl-card__title-text white_text">
                        Groups
                    </h2>
                </div>
                <div className="mdl-layout-spacer"></div>
                <div className="mdl-cell mdl-cell--1-col">
                    <button onClick={this.contract} className="mdl-button mdl-js-button mdl-button--fab mdl-js-ripple-effect mdl-button--colored">
                      <i className="material-icons">remove</i>
                    </button>
                </div>
            </div>
            <div className="mdl-card__supporting-text">
                Upon creation surveys are sent to a group to be answered by it's members. Groups 
                are user created and in order to respond to a survey you must be subscribed to the
                group the survey was sent to.
            </div>
            <div className="mdl-card__title mdl-color--accent">
                <h2 className="mdl-card__title-text">
                    Group Creation
                </h2>
            </div>
            <div className="mdl-card__supporting-text">
                First navigate to the Group page through the navigation bar. You will see several
                fields, you'll need to enter a unique group name at the top as well as  users that 
                you wish to invite to your new group upon creation in the fields below. Additional 
                fields to invite users will appear as you fill them out. Click Submit when you're 
                finished!
            </div>
            <div className="mdl-card__title mdl-color--accent">
                <h2 className="mdl-card__title-text">
                    Group Management
                </h2>
            </div>
            <div className="mdl-card__supporting-text">
                First navigate to the Profile page through the navigation bar. You'll see a My Groups 
                section as well as a Subscribe to a Group section at the bottom of the page. If you 
                want to unsubscribe from a group and no longer be able to see or reply to that groups
                surveys, click the orange Unsubscribe button to the right of the group. If you wish to 
                see and be able to responsd to a groups surveys you must enter the groups name into the
                field labeled "GroupID here..." and then click the orange Subscribe button. 
            </div>
          </div>
        );
    }
    else{
        return(
        <div className="groupsHelpDiv mdl-card mdl-shadow--2dp mdl-cell mdl-cell--12-col">
            <div className="mdl-card__title mdl-color--primary">
                <div className="mdl-cell mdl-cell--6-col">
                    <h2 className="mdl-card__title-text white_text">
                        Groups
                    </h2>
                </div>
                <div className="mdl-layout-spacer"></div>
                <div className="mdl-cell mdl-cell--1-col">
                    <button onClick={this.expand} className="mdl-button mdl-js-button mdl-button--fab mdl-js-ripple-effect mdl-button--colored">
                      <i className="material-icons">add</i>
                    </button>
                </div>
            </div>
        </div>
        );
    }
    }
});

var SurveysHelp = React.createClass({

    getInitialState: function(){
        return({
            expanded: "false"
        });
    },
    
    expand: function(){
        this.setState({
            expanded: "true"
        });
    },
    
    contract: function(){
        this.setState({
            expanded: "false"
        });
    },
    
    render:function(){
    if(this.state.expanded == "true"){
        return(
              <div className="mdl-card mdl-shadow--2dp mdl-cell mdl-cell--12-col">
                <div className="mdl-card__title mdl-color--primary">
                    <div className="mdl-cell mdl-cell--6-col">
                        <h2 className="mdl-card__title-text white_text">
                            Surveys
                        </h2>
                    </div>
                    <div className="mdl-layout-spacer"></div>
                    <div className="mdl-cell mdl-cell--1-col">
                        <button onClick={this.contract} className="mdl-button mdl-js-button mdl-button--fab mdl-js-ripple-effect mdl-button--colored">
                          <i className="material-icons">remove</i>
                        </button>
                    </div>
                </div>
                <div className="mdl-card__supporting-text">
                    Surveys are a collection of Free Response, Multiple Choice, Single Choice, and Rating
                    questions that can be sent to a group. 
                </div>
                <div className="mdl-card__title mdl-color--accent">
                    <h2 className="mdl-card__title-text">
                        Creating a Survey
                    </h2>
                </div>
                <div className="mdl-card__supporting-text">
                    First navigate to the Surveys page through the navigation bar. At the top of the Create a Survey section
                    you'll see a field labeled "Search for Group here...", you'll have to search for the group you want the
                    survey to be sent to by typing in at least part of the name of the group and then clicking Search. After 
                    searching a number of buttons will appear with group names on them, click the button corresponding to the
                    group you want to send the survey to. Next type in the name for your survey in the field under the label
                    Survey Title. Next start creating your questions, for each question you'll have to fill in a title for 
                    the question in the field labeled "Question title", then select a question type from the drop down menu
                    right below next to the label "Type: ", if you choose Single Choice or Multiple Choice you'll need to add
                    options, to add additional options (you need at least two) click the + button next to "Add Option", name the
                    options by filling in their fields. 
                </div>
                <div className="mdl-card__title mdl-color--accent">
                    <h2 className="mdl-card__title-text">
                        Responding to a Survey
                    </h2>
                </div>
                <div className="mdl-card__supporting-text">
                    First navigate to the Home page through the navigation bar. If you belong to a Group which has a survey
                    you have yet to respond to it will be displayed on the page. Fill in your answers to 
                    each question and push Next until you've answered every question upon which you can click 
                    Submit. At any time you can traverse to other questions and change your answers, upon 
                    submission however your answers will be final.
                </div>
                <div className="mdl-card__title mdl-color--accent">
                    <h2 className="mdl-card__title-text">
                        Question Types
                    </h2>
                </div>
                <div className="mdl-card__supporting-text">
                    <ul className="mdl-list">
                        <li className="mdl-list__item">
                            Multiple Choice: A question with multiple checkboxes, you can choose more than one answer
                        </li>
                        <li className="mdl-list__item">
                            Single Choice: A question with multiple checkboxes, you can only choose one answer
                        </li>
                        <li className="mdl-list__item">
                            Rating Scale: A question with a slider, you can drag the slider to answer the question with
                            some value between 0 and 10
                        </li>
                        <li className="mdl-list__item">
                            Free Response: A question with a textbox, you type in your response to the question 
                        </li>
                    </ul>
                </div>
              </div>
        );
    }
    else{
        return(
        <div className="surveysHelpDiv mdl-card mdl-shadow--2dp mdl-cell mdl-cell--12-col">
            <div className="mdl-card__title mdl-color--primary">
                <div className="mdl-cell mdl-cell--6-col">
                    <h2 className="mdl-card__title-text white_text">
                        Surveys
                    </h2>
                </div>
                <div className="mdl-layout-spacer"></div>
                <div className="mdl-cell mdl-cell--1-col">
                    <button onClick={this.expand} className="mdl-button mdl-js-button mdl-button--fab mdl-js-ripple-effect mdl-button--colored">
                      <i className="material-icons">add</i>
                    </button>
                </div>
            </div>
        </div>
        );
    }
    }
});

var Censorship = React.createClass({

    getInitialState: function(){
        return({
            expanded: "false"
        });
    },
    
    expand: function(){
        this.setState({
            expanded: "true"
        });
    },
    
    contract: function(){
        this.setState({
            expanded: "false"
        });
    },
    
    render:function(){
    if(this.state.expanded=="true"){
        return(
          <div className="mdl-card mdl-shadow--2dp mdl-cell mdl-cell--12-col">
            <div className="mdl-card__title mdl-color--primary">
                <div className="mdl-cell mdl-cell--6-col">
                    <h2 className="mdl-card__title-text white_text">
                        Censorship Policy
                    </h2>
                </div>
                <div className="mdl-layout-spacer"></div>
                <div className="mdl-cell mdl-cell--1-col">
                    <button onClick={this.contract} className="mdl-button mdl-js-button mdl-button--fab mdl-js-ripple-effect mdl-button--colored">
                      <i className="material-icons">remove</i>
                    </button>
                </div>
            </div>
            <div className="mdl-card__supporting-text">
                TBD
            </div>
          </div>
        );
    }
        
    else{
        return(
        <div className="censorshipDiv mdl-card mdl-shadow--2dp mdl-cell mdl-cell--12-col">
            <div className="mdl-card__title mdl-color--primary">
                <div className="mdl-cell mdl-cell--6-col">
                    <h2 className="mdl-card__title-text white_text">
                        Censorship Policy
                    </h2>
                </div>
                <div className="mdl-layout-spacer"></div>
                <div className="mdl-cell mdl-cell--1-col">
                    <button onClick={this.expand} className="mdl-button mdl-js-button mdl-button--fab mdl-js-ripple-effect mdl-button--colored">
                      <i className="material-icons">add</i>
                    </button>
                </div>
            </div>
        </div>
        );
    }
    }
});

var InformationCollection = React.createClass({

    getInitialState: function(){
        return({
            expanded: "false"
        });
    },
    
    expand: function(){
        this.setState({
            expanded: "true"
        });
    },
    
    contract: function(){
        this.setState({
            expanded: "false"
        });
    },
    
    render:function(){
    if(this.state.expanded=="true"){
        return(
          <div className="mdl-card mdl-shadow--2dp mdl-cell mdl-cell--12-col">
            <div className="mdl-card__title mdl-color--primary">
                <div className="mdl-cell mdl-cell--6-col">
                    <h2 className="mdl-card__title-text white_text">
                        Information Collection Policy
                    </h2>
                </div>
                <div className="mdl-layout-spacer"></div>
                <div className="mdl-cell mdl-cell--1-col">
                    <button onClick={this.contract} className="mdl-button mdl-js-button mdl-button--fab mdl-js-ripple-effect mdl-button--colored">
                      <i className="material-icons">remove</i>
                    </button>
                </div>
            </div>
            <div className="mdl-card__supporting-text">
                TBD
            </div>
          </div>
        );
    }
    else{
        return(
        <div className="informationCollectionDiv mdl-card mdl-shadow--2dp mdl-cell mdl-cell--12-col">
            <div className="mdl-card__title mdl-color--primary">
                <div className="mdl-cell mdl-cell--6-col">
                    <h2 className="mdl-card__title-text white_text">
                        Information Collection Policy
                    </h2>
                </div>
                <div className="mdl-layout-spacer"></div>
                <div className="mdl-cell mdl-cell--1-col">
                    <button onClick={this.expand} className="mdl-button mdl-js-button mdl-button--fab mdl-js-ripple-effect mdl-button--colored">
                      <i className="material-icons">add</i>
                    </button>
                </div>
            </div>
        </div>
        );
    }
    }
})