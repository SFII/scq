var SearchCard = React.createclass({
    getInitialState: function(){
        return{
            search_item: '',
        }
    },

    handleSearchItemChange: function(event) {
        this.setState({search_item: event.target.value});
    },

    onSearch: function(){

        var searchObj = {
            "searchtype": "Group",
            "searchstring": this.state.search_item,
            "requestedfields": ["id"]
        };
        
        $.ajax({
            url: this.props.routes.search,
            contentType: 'application/json',
            type: 'POST',
            data: JSON.stringify(searchObj),
            success: function(data){
                console.log('Post success');
            }.bind(this),
            error: function(xhr, status,err){
                console.error("/api/response", status, err.toString());
            }.bind(this)
            });
    },
    
    render: function(){
    <div className="mdl-card mdl-shadow--2dp mdl-cell mdl-cell--4-col mdl-cell--8-tablet mdl-cell--12-col-desktop">
        
        <input className="mdl-textfield__input"
            type="text"
            value={this.state.search_item}
            onChange={this.handleSearchItemChange}/>
        
        <button onClick={this.onSearch} className="mdl-cell mdl-cell--4-col mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--accent right_button">
              SEARCH
        </button>
    </div
}
});