var SearchCard = React.createClass({
    getInitialState: function(){
        return{
            search_item: "",
            search_item_type: "Group",
            requestedfields: ["id"],
            search_results: [],
            recipient: "",
            showResults: 0
        }
    },

    handleSearchItemChange: function(event) {
        this.setState({search_item: event.target.value});
    },

    onSearch: function(){

        this.setState({showResults: 1});
        var searchObj = {
            "searchtype": this.state.search_item_type,
            "searchstring": this.state.search_item,
            "requestedfields": this.state.requestedfields
        };
        
        $.ajax({
            url: this.props.routes.search,
            contentType: 'application/json',
            type: 'POST',
            dataType:  "json",
            data: JSON.stringify(searchObj),
            success: function(data){
                this.setState({search_results:data});
            }.bind(this),
            error: function(xhr, status,err){
                console.error("/api/response", status, err.toString());
            }.bind(this)
            });
    },
    
    handleSearchItemTypeChange: function(event){
        this.setState({search_item_type:event.target.value});
        if(event.target.value == "Group"){
            this.setState({requestedfields: ["id"]})
        }
        else if(event.target.value == "User"){
            this.setState({requestedfields: ["username"]})
        }
    },
    
    setRecipient: function(surveyRecipient){
        this.setState({recipient: surveyRecipient});
        this.props.setRecipient(surveyRecipient, this.state.search_item_type);
        this.setState({showResults: 0});
    },
    
    render: function(){
    
    var renderedSearchResults = this.state.search_results.map((result) => {
        if(this.state.search_results.length > 0 && this.state.showResults == 1){
            if(this.state.search_item_type=="Group"){
                return(
                <GroupResultDiv key={result.id} setRecipient = {this.setRecipient} resultInfo={result}/>
                )
            }
            else if(this.state.search_item_type=="User"){
                return(
                <UserResultDiv key={result.username} setRecipient = {this.setRecipient} resultInfo={result}/>
                )
            }
        }
    });
/*
        Put this back in if we want to be able to send to users
            <!-- <p className="mdl-cell mdl-cell--12-col">Type:
                    <select
                    id="UserOrGroupSelect"
                    onChange={this.handleSearchItemTypeChange}
                    value={this.state.value}>
                        <option value="Group">Group</option>
                        <option value="User">User</option>
                    </select>
            </p> -->
*/    
    return(
        <div className="searchCardDiv mdl-grid mdl-card__title mdl-card--expand mdl-300">
            <div className="mdl-cell mdl-cell--12-col">
                Post to Group: {this.state.recipient}
            </div>
            <span>
                <div className="mdl-textfield mdl-js-textfield mdl-cell mdl-cell--8-col">
                    <input className="mdl-textfield__input"
                    type="text" 
                    value={this.state.search_item} 
                    onChange={this.handleSearchItemChange}/>
                    <label className="mdl-textfield__label">Search for group here...</label>
                </div>
                <button className="mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--accent mdl-cell mdl-cell--4-col" onClick={this.onSearch}>
                    SEARCH
                </button>
            </span>
            <div className="mdl-cell mdl-cell--12-col"></div>
            {renderedSearchResults}
        </div>
    );
}
});

var GroupResultDiv = React.createClass({
    
    getInitialState: function(){
        return{
            showResult: 1
        }
    },
    
    setRecipient: function(){
        this.props.setRecipient(this.props.resultInfo.id);
        this.setState({showResult: 0})
    },
    
    render: function(){
        if(this.state.showResult==1){
            return(
                <button className="mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--accent mdl-cell mdl-cell--4-col" onClick={this.setRecipient}>
                    {this.props.resultInfo.id}
                </button>
            );
        }
        else{
            return(
                <div></div>
            );
        }
    }
    
});

var UserResultDiv = React.createClass({
    
    getInitialState: function(){
        return{
            showResult: 1
        }
    },
    
    setRecipient: function(){
        this.props.setRecipient(this.props.resultInfo.username);
        this.setState({showResult: 0})
    },
    
    render: function(){
        if(this.state.showResult==1){
            return(
                <button className="mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--accent mdl-cell mdl-cell--4-col" onClick={this.setRecipient}>
                    {this.props.resultInfo.username}
                </button>
            );
        }
        else{
            return(
                <div></div>
            );
        }
    }  
});
