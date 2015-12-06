var Welcome = React.createClass({
	render: function() {
		return (
		<div>
			<About />
 			<Login />
		</div>
		);
	}
});

var About = React.createClass({
	render: function() {
		return (
				<div className="updates mdl-card mdl-shadow--2dp mdl-cell mdl-cell--8-col">
				<p>Campus Consensus is a survey and data collection
			system developed for improving student-faculty
			relationships at universities being developed at
			University Colorado at Boulder. Our platform allows
			students and faculty to ask questions and offer short
			surveys to improve instructional quality, align
			student and faculty interests, and express consensus
			about campus issues.</p>
				<p>Students in the same class or department can learn
			about how other students feel about the quality of the
			course or what is working and what is not. Similarly,
			faculty can get fine-grain information about how their
			instruction is being received by their students.</p>
				<p>Our data will be available to the entire campus in
			an anonymous form. The project is being developed by
			computer science seniors at University of Colorado
			Boulder.</p>
				<p>Please contact our project leads with any
			questions:</p>
				<ul>
				<li>antsankov [at] gmail [dot] com</li>
				<li>michael [dot] skirpan [at] colorado [dot] edu</li>
				</ul>
				</div>
		);
	}
});

var Login = React.createClass({
	render: function() {
		return (
				<div className="updates mdl-card mdl-shadow--2dp mdl-cell mdl-cell--4-col">
				<form action="/register/culdap" method="post">
				<label>CU Login Name</label>
				<input type="text" name="username" required/>
				<label>Password</label>
				<input type="password" name="password" required/>
				<input type="submit" id="loginbtn" name="login" value="Log In" class="button"/>
				</form>
				</div>
		);
	}
});
