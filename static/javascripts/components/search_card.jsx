var SearchCard = React.createClass({
    getInitialState: function(){
        return{
            search_item: "",
            search_item_type: "Group",
            requestedfields: ["id"],
            search_results: []
        }
    },

    handleSearchItemChange: function(event) {
        this.setState({search_item: event.target.value});
    },

    onSearch: function(){

        var searchObj = {
            "searchtype": this.state.search_item_type,
            "searchstring": this.state.search_item,
            "requestedfields": this.state.requestedfields
        };
        
        console.log(searchObj);
        
        $.ajax({
            url: this.props.routes.search,
            contentType: 'application/json',
            type: 'POST',
            data: JSON.stringify(searchObj),
            success: function(data){
                console.log(Object.prototype.toString.call(data))
                console.log(data);
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
    
    appendToSendList: function(surveyRecipient){
        search_results = this.state.search_results;
        search_results.append(surveyRecipient);
        this.setState({search_results: search_results});
        console.log(search_results);
    },
    
    render: function(){
    console.log(this.state.search_results);
    var renderedSearchResults = this.state.search_results.map((result) => {
        if(this.state.search_results > 0){
            if(this.state.search_item_type=="Group"){
                return(
                    <GroupResultDiv key={result.id} onAppend = {this.appendToSendList} resultInfo={result}/>
                );
            }
            else if(this.state.search_item_type=="User"){
                return(
                <UserResultDiv key={result.id} onAppend={this.appendToSendList} resultInfo={result}/>
                );
            }
        }
    });
    return(
    <div className="mdl-grid mdl-card__title mdl-card--expand mdl-300">
        <p className="mdl-cell mdl-cell--12-col">Type:
            <select
            id="UserOrGroupSelect"
            onChange={this.handleSearchItemTypeChange}
            value={this.state.value}>
                <option value="Group">Group</option>
                <option value="User">User</option>
            </select>
        </p>
        
        <span>
          <div className="mdl-textfield mdl-js-textfield mdl-cell mdl-cell--8-col">
              <input className="mdl-textfield__input"
              type="text" 
              value={this.state.search_item} 
              onChange={this.handleSearchItemChange}/>
              <label className="mdl-textfield__label">Search here...</label>
          </div>
          <button className="mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--accent mdl-cell mdl-cell--4-col" onClick={this.onSearch}>
                SEARCH
          </button>
        </span>
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
    
    onAppend: function(){
        this.props.onAppend(this.props.resultInfo);
        this.setState({showResult: 0})
    },
    
    render: function(){
        if(this.state.showResult==1){
            return(
                <button className="mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--accent mdl-cell mdl-cell--4-col" onClick={this.onAppend()}>
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
    
    onAppend: function(){
        this.props.onAppend(this.props.resultInfo);
        this.setState({showResult: 0})
    },
    
    render: function(){
        if(this.state.showResult==1){
            return(
                <button className="mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--accent mdl-cell mdl-cell--4-col" onClick={this.onAppend()}>
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
