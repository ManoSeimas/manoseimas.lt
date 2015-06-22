var PaliamentarianRow = React.createClass({
  render: function() {
    var parliamentarian = this.props.obj;
    return (
      <div className="ui parliamentarian-row zero margin page grid">
        <div className="name eight wide column">
          <img className="photo" src={parliamentarian.photo}></img>
          <div className="info">
            <h2><a href={parliamentarian.url}>{parliamentarian.full_name}</a></h2>
            <p><a href={parliamentarian.fraction_url}>{parliamentarian.fraction_name}</a></p>
          </div>
        </div>
        <div className="two wide column">
          <div className="ui discussion statistic">
            <div className="value">{parliamentarian.statement_count}</div>
            <div className="label">pasisakymai</div>
          </div>
        </div>
        <div className="two wide column">
          <div className="ui projects statistic">
            <div className="value">{parliamentarian.passed_law_project_ratio}%</div>
            <div className="label">sėkmingų projektų</div>
          </div>
        </div>
        <div className="two wide column">
          <div className="ui voting statistic">
            <div className="value">{parliamentarian.vote_percentage}%</div>
            <div className="label">balsavimų</div>
          </div>
        </div>
      </div>
    )
  }
});

var FractionRow = React.createClass({
  render: function() {
    var fraction = this.props.obj;
    return (
      <div className="ui fraction-row zero margin page grid">
        <div className="name eight wide column">
          <img className="logo" src={fraction.logo_url}></img>
          <div className="info">
            <h2><a href={fraction.url}>{fraction.name}</a></h2>
          </div>
        </div>
        <div className="two wide column">
          <div className="ui member statistic">
            <div className="value">{fraction.member_count}</div>
            <div className="label">narių</div>
          </div>
        </div>
        <div className="two wide column">
          <div className="ui discussion statistic">
            <div className="value">{fraction.avg_statement_count}</div>
            <div className="label">pasisakymai</div>
          </div>
        </div>
        <div className="two wide column">
          <div className="ui projects statistic">
            <div className="value">{fraction.avg_passed_law_project_ratio}%</div>
            <div className="label">sėkmingų projektų</div>
          </div>
        </div>
        <div className="two wide column">
          <div className="ui voting statistic">
            <div className="value">{fraction.avg_vote_percentage}%</div>
            <div className="label">balsavimų vid.</div>
          </div>
        </div>
      </div>
    )
  }
});
