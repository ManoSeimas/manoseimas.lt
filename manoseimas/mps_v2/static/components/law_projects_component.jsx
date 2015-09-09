var LawProjects = React.createClass({
  getInitialState: function() {
    return {
      projects: [],
      current_page: 1,
      items_per_page: 15,
      show_only_selected: false,
      loaded: false
    }
  },

  componentDidMount: function() {
    $.get(this.props.data_url, function(result) {
      if (this.isMounted()) {
        this.setState({
          projects: result.items,
          loaded: true
        })
      }
    }.bind(this))
  },

  onChangePage: function(page) {
    this.setState({current_page: page});
    $.scrollTo('.law-projects', 100, {offset: -40});
  },

  showPassedOnly: function() {
    this.setState({
      show_only_selected: !this.state.show_only_selected,
      current_page: 1
    });
  },

  render: function() {
    var columns = {
      number: {
        title: 'Projekto numeris',
        func: function (item) {
          return <a href={item['url']} target='_blank'>{item['number']}</a>
        }
      },
      title: {title: 'Pavadinimas', className: 'center aligned', itemClassName: 'left aligned', func: null},
      date: {title: 'Teikimo data', className: 'date center aligned', itemClassName: 'center aligned', func: null},
      proposer_count: {title: 'Viso teikėjų', className: 'center aligned', itemClassName: 'center aligned', func: null},
      date_passed: {
        title: 'Stadija',
        className: 'center aligned',
        itemClassName: 'center aligned',
        func: function (item) {
          return (item['date_passed']) ? 'Priimta '+item['date_passed'] : 'Nepriimta'
        }
      },
    }

    var projects = this.state.projects;
    if (this.state.show_only_selected) {
      projects = projects.filter(function(item) {
        return item.date_passed
      }.bind(this))
    }

    var slice_from = (this.state.current_page-1)*this.state.items_per_page,
        slice_to = this.state.current_page*this.state.items_per_page,
        total_pages = Math.round((projects.length / this.state.items_per_page)+0.5);

    return (
      <div className="law-projects">
        <div className="ui page grid">
          <div className="eight wide column">
            <h2 className="title">Teisės aktai</h2>
          </div>
          <div className="eight wide right aligned column">
            <div className="ui toggle checkbox" onClick={this.showPassedOnly}>
              <input name="filter_passed" type="checkbox" checked={this.state.show_only_selected}/>
              <label>Rodyti tik priimtus projektus</label>
            </div>
          </div>

          <Loader loaded={this.state.loaded}>
            <div className="ui zero margin grid">
              <SemanticTable columns={columns}
                             items={projects.slice(slice_from, slice_to)} />
            </div>
            <div className="ui center aligned grid">
              <Paginator max={total_pages} onChange={this.onChangePage} />
            </div>
          </Loader>
        </div>
      </div>
    )
  }
});

var SemanticTable = React.createClass({
  render: function() {
    var columns = this.props.columns;
    return (
      <table className="ui zero paddings table">
        <thead>
          <tr>
            {Object.keys(columns).map(function (key) {
              return <th className={columns[key].className}>{columns[key].title}</th>
            })}
          </tr>
        </thead>
        <tbody>
            {this.props.items.map(function (item) {
              return (
                <tr>
                  {Object.keys(columns).map(function (key) {
                    return (
                      <td className={columns[key].itemClassName}>
                      {(columns[key].func) ? columns[key].func(item) : item[key]}
                      </td>
                    )
                  })}
                </tr>
              )
            })}
        </tbody>
      </table>
    )
  }
});


var data_url = '/json/law_projects/' + $('#law-projects-component').attr("data-slug");

React.render(
  <LawProjects data_url={data_url} />,
  document.getElementById('law-projects-component')
);
