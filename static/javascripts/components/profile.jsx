var ProfilePage = React.createClass({
  getInitialState: function(){
    var subscribed_groups = '';
    var user_status = '';
    var num_sub_groups = user_data[0].subscribed_groups.length;
    if ((num_sub_groups == 0) || (user_data[0].subscribed_groups == [''])) {
      subscribed_groups = '';
    } else {
      for (var i = 0; i < num_sub_groups; i++) {
        subscribed_groups += user_data[0].subscribed_groups[i];
        if (i < num_sub_groups - 1) {
          subscribed_groups += "\n";
        }
      }
    }
    if (user_data[0].primary_affiliation == "Student") {
      if (user_data[0].status) {
        user_status = user_data[0].status;
      } else {
        user_status = "Did not specify academic year";
      }
    }
    return {
      username: user_data[0].username,
      user_affiliation: user_data[0].primary_affiliation,
      email: user_data[0].email,
      dob: user_data[0].dob,
      user_gender: user_data[0].gender,
      user_ethnicity: user_data[0].ethnicity,
      user_native_language: user_data[0].native_language,
      user_status: user_data[0].status,
      subscribed_groups: subscribed_groups,
      affiliation: extra_data[0].primary_affiliation,
      gender: extra_data[0].gender,
      ethnicity: extra_data[0].ethnicity,
      native_language: extra_data[0].native_language,
      status: extra_data[0].status,

    };
  },
  handleChange: function(key) {
    return function (e) {
      var state = {};
      state[key] = e.target.value;
      this.setState(state);
    }.bind(this);
  },
  render: function(){
    var style = {
      listStyleType: "none",
      fontSize: "20px"
    };
    return(
      <ul style={style}>
      <form action="/profile" method="post">
        Username: <input value={this.state.username} readOnly /><br/>
        Affiliation(s): <select>
                          <option value={this.state.user_affiliation}>{this.state.user_affiliation}</option>
                          <option value={this.state.affiliation}>{this.state.affiliation[0]}</option>
                          <option value={this.state.affiliation}>{this.state.affiliation[1]}</option>
                        </select><br/>
        Email: <input value={this.state.email} onChange={this.handleChange('email')} required /><br/>
        Birth Date: <input type="date" value={this.state.dob} onChange={this.handleChange('dob')} required /><br/>
        Gender: <select>
                  <option value={this.state.user_gender}>{this.state.user_gender}</option>
                  <option value={this.state.gender}>{this.state.gender[0]}</option>
                </select><br/>
        Ethnicity: <select>
                     <option value={this.state.user_ethnicity}>{this.state.user_ethnicity}</option>
                     <option value={this.state.ethnicity}>{this.state.ethnicity[0]}</option>
                     <option value={this.state.ethnicity}>{this.state.ethnicity[1]}</option>
                     <option value={this.state.ethnicity}>{this.state.ethnicity[2]}</option>
                     <option value={this.state.ethnicity}>{this.state.ethnicity[3]}</option>
                     <option value={this.state.ethnicity}>{this.state.ethnicity[4]}</option>
                     <option value={this.state.ethnicity}>{this.state.ethnicity[5]}</option>
                     <option value={this.state.ethnicity}>{this.state.ethnicity[6]}</option>
                   </select><br/>
        Native Language: <select>
                           <option value={this.state.user_native_language}>{this.state.user_native_language}</option>
                           <option value={this.state.native_language}>{this.state.native_language[0]}</option>
                           <option value={this.state.native_language}>{this.state.native_language[1]}</option>
                           <option value={this.state.native_language}>{this.state.native_language[2]}</option>
                           <option value={this.state.native_language}>{this.state.native_language[3]}</option>
                           <option value={this.state.native_language}>{this.state.native_language[4]}</option>
                           <option value={this.state.native_language}>{this.state.native_language[5]}</option>
                           <option value={this.state.native_language}>{this.state.native_language[6]}</option>
                           <option value={this.state.native_language}>{this.state.native_language[7]}</option>
                           <option value={this.state.native_language}>{this.state.native_language[8]}</option>
                           <option value={this.state.native_language}>{this.state.native_language[9]}</option>
                           <option value={this.state.native_language}>{this.state.native_language[10]}</option>
                           <option value={this.state.native_language}>{this.state.native_language[11]}</option>
                         </select><br/>
        Academic Year: <select>
                         <option value={this.state.user_status}>{this.state.user_status}</option>
                         <option value={this.state.status}>{this.state.status[0]}</option>
                         <option value={this.state.status}>{this.state.status[1]}</option>
                         <option value={this.state.status}>{this.state.status[2]}</option>
                       </select><br/>
        Group(s) Subscribed: <br/><textarea name="courses" cols="30" rows="5" value={this.state.subscribed_groups}
                                    onChange={this.handleChange('subscribed_groups')} /><br/>
        <br/>
        <input type="submit" value="submit" />
      </form>
      </ul>
    );
  }
});
