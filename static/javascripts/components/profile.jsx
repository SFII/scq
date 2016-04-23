var ProfilePage = React.createClass({
  getInitialState: function(){
    var user_affiliation = user_data[0].primary_affiliation;
    var user_gender = user_data[0].gender;
    var user_ethnicity = user_data[0].ethnicity;
    var user_native_language = user_data[0].native_language;
    if(test == false){
	    var affiliation = _.pull(extra_data[0].primary_affiliation, user_affiliation);
	    var gender = _.pull(extra_data[0].gender, user_gender);
	    var ethnicity = _.pull(extra_data[0].ethnicity, user_ethnicity);
	    var native_language = _.pull(extra_data[0].native_language, user_native_language);
    }
    var user_status = null;
    var status = null;
    if (user_affiliation == "Student" || user_affiliation == "Both") {
      var user_status = user_data[0].status;
      if(test == false){
      var status = _.pull(extra_data[0].status, user_status);
      }
      else{
      var status = "test status"
      }
    }
    return {
      username: user_data[0].username,
      email: user_data[0].email,
      dob: user_data[0].dob,
      user_affiliation,
      user_gender,
      user_ethnicity,
      user_native_language,
      user_status,
      affiliation,
      gender,
      ethnicity,
      native_language,
      status,
      edit: false
    };
  },
  handleChange: function(key) {
    return function (e) {
      var state = {};
      state[key] = e.target.value;
      this.setState(state);
    }.bind(this);
  },
  handleClick: function(event) {
    this.setState({edit: !this.state.edit});
  },
  render: function(){
    var style = {
      listStyleType: "none",
      fontSize: "20px"
    };
    var academic_year = null;
    if (this.state.user_affiliation != "Faculty") {
      academic_year = (<li>Academic Year: {this.state.user_status}</li>);
    }
    if (this.state.edit == false) {
      return(
        <ul className="profilePageDiv" style={style}>
          <button type="button" onClick={this.handleClick}>edit</button><br/>
          <li>Username: {this.state.username}</li>
          <li>Affiliation: {this.state.user_affiliation}</li>
          <li>Email: {this.state.email}</li>
          <li>Birth Date: {this.state.dob}</li>
          <li>Gender: {this.state.user_gender}</li>
          <li>Ethnicity: {this.state.user_ethnicity}</li>
          <li>Native Language: {this.state.user_native_language}</li>
          {academic_year}
        </ul>
      );
    } else {
      var academic_year_options = null;
      if (this.state.user_affiliation != "Faculty") {
        academic_year_options = (
          <li>Academic Year: <select name="status">
                               <option value={this.state.user_status}>{this.state.user_status}</option>
                               <option value={this.state.status[0]}>{this.state.status[0]}</option>
                               <option value={this.state.status[1]}>{this.state.status[1]}</option>
                               <option value={this.state.status[2]}>{this.state.status[2]}</option>
                               <option value={this.state.status[3]}>{this.state.status[3]}</option>
                               <option value={this.state.status[4]}>{this.state.status[4]}</option>
                             </select></li>
        );
      }
      return(
        <ul style={style}>
        <form action="/profile" method="post">
          <button type="button" onClick={this.handleClick}>edit</button><br/>
          Username: <input name="username" value={this.state.username} readOnly /><br/>
          Affiliation(s): <select name="primary_affiliation">
                            <option value={this.state.user_affiliation}>{this.state.user_affiliation}</option>
                            <option value={this.state.affiliation[0]}>{this.state.affiliation[0]}</option>
                            <option value={this.state.affiliation[1]}>{this.state.affiliation[1]}</option>
                          </select><br/>
          Email: <input type="email" name="email" value={this.state.email} onChange={this.handleChange('email')} required /><br/>
          Birth Date: <input type="date" name="dob" value={this.state.dob} onChange={this.handleChange('dob')} required /><br/>
          Gender: <select name="gender">
                    <option value={this.state.user_gender}>{this.state.user_gender}</option>
                    <option value={this.state.gender[0]}>{this.state.gender[0]}</option>
                    <option value={this.state.gender[1]}>{this.state.gender[1]}</option>
                    <option value={this.state.gender[2]}>{this.state.gender[2]}</option>
                  </select><br/>
          Ethnicity: <select name="ethnicity">
                       <option value={this.state.user_ethnicity}>{this.state.user_ethnicity}</option>
                       <option value={this.state.ethnicity[0]}>{this.state.ethnicity[0]}</option>
                       <option value={this.state.ethnicity[1]}>{this.state.ethnicity[1]}</option>
                       <option value={this.state.ethnicity[2]}>{this.state.ethnicity[2]}</option>
                       <option value={this.state.ethnicity[3]}>{this.state.ethnicity[3]}</option>
                       <option value={this.state.ethnicity[4]}>{this.state.ethnicity[4]}</option>
                       <option value={this.state.ethnicity[5]}>{this.state.ethnicity[5]}</option>
                       <option value={this.state.ethnicity[6]}>{this.state.ethnicity[6]}</option>
                     </select><br/>
          Native Language: <select name="native_language">
                             <option value={this.state.user_native_language}>{this.state.user_native_language}</option>
                             <option value={this.state.native_language[0]}>{this.state.native_language[0]}</option>
                             <option value={this.state.native_language[1]}>{this.state.native_language[1]}</option>
                             <option value={this.state.native_language[2]}>{this.state.native_language[2]}</option>
                             <option value={this.state.native_language[3]}>{this.state.native_language[3]}</option>
                             <option value={this.state.native_language[4]}>{this.state.native_language[4]}</option>
                             <option value={this.state.native_language[5]}>{this.state.native_language[5]}</option>
                             <option value={this.state.native_language[6]}>{this.state.native_language[6]}</option>
                             <option value={this.state.native_language[7]}>{this.state.native_language[7]}</option>
                             <option value={this.state.native_language[8]}>{this.state.native_language[8]}</option>
                             <option value={this.state.native_language[9]}>{this.state.native_language[9]}</option>
                             <option value={this.state.native_language[10]}>{this.state.native_language[10]}</option>
                             <option value={this.state.native_language[11]}>{this.state.native_language[11]}</option>
                           </select><br/>
          {academic_year_options}
          <br/>
          <input type="submit" value="submit" />
        </form>
        </ul>
      );
    }
  }
});
