var GroupsPage = React.createClass({
    render: function() {
        return (
            <div>
                <div>
                    <CreateGroup/>
                    <BrowseGroups/>
                </div>
            </div>
        )
    }
});

var CreateGroup = React.createClass({
    render: function() {
        var style = {
            marginTop: "5px",
            marginBottom: "5px"
        }
        return (
            <div style={style}>
                <h3>Create a group:</h3>
                <div className="mdl-grid">
                    <div className="mdl-cell mdl-cell--1-col">
                    </div>
                    <div className="mdl-cell mdl-cell--11-col">
                        <form action="/api/groups" method="POST">
                            <div className="mdl-textfield
                                            mdl-js-textfield
                                            mdl-textfield--floating-label">
                                <input style={{fontSize: "24px"}}
                                       type="text" name="groupname"
                                       className="mdl-textfield__input"></input>
                                <label className="mdl-textfield__label"
                                       htmlFor="groupname">Group Name</label>
                            </div>
                            <GroupMembers/>
                            <input className="mdl-button
                                              mdl-js-button
                                              mdl-button--raised
                                              mdl-js-ripple-effect"
                                   type="submit" value="Submit"></input>
                        </form>
                    </div>
                </div>
            </div>
        )
    }
});

var GroupMembers = React.createClass({
    getInitialState: function() {
        return({
            members: [user_data[0].username]
        })
    },

    newMember:  function(e) {
        this.setState(function(state){
            state.members.push(e.target.value);
        });
    },
    render: function() {
        var memberlist = [];
        var count = this.state.members.length
        var element = function(key, user) {
            return <div key={key}>
                <div className="mdl-textfield" key={i}>
                    <input type="text"
                           name="members"
                           className="mdl-textfield__input memberlist"
                           defaultValue={user} >
                    </input>
                </div>
            </div>;
        }
        for(var i = 0; i < count; i++) {
            memberlist.push(element(i, this.state.members[i]));
        }
        memberlist.push(
            <div className="mdl-textfield" key={i}>
                <input type="text"
                       name="person"
                       className="mdl-textfield__input memberlist"
                       defaultValue={""}
                       onChange={this.newMember}>
                </input></div>);
        return (
            <div>
                <h4>Members</h4>
                Add initial members here, but anyone can join
                {memberlist}
            </div>
        )
    }
});

var BrowseGroups = React.createClass({
    render: function() {
        return <div></div>
    }
});
