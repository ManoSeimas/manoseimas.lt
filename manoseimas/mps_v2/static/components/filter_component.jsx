var SortebleList = React.createClass({
  getInitialState: function() {
    return {
      items: [],
      current_page: 1,
      items_per_page: 10,
      sort_key: null,
      filter_selected: 'all',
      filter_options: null,
      loaded: false
    };
  },

  componentDidMount: function() {
    if (this.isMounted()) this.loadData(this.props.endpoint);
  },

  loadData: function(endpoint) {
    $.get(endpoint, function(result) {
      this.setState({
        items: result.items,
        loaded: true,
        filter_options: (this.props.sidebar_filter) ? this.props.sidebar_filter.options_func(result.items) : null
      });
    }.bind(this))
  },

  componentWillReceiveProps: function (nextProps) {
    this.setState({loaded: false, current_page: 1});
    this.loadData(nextProps.endpoint);
  },

  sortElements: function (param) {
    var self = this;
    return function () {
      self.setState({
        items: self.state.items.sort(function (a, b) {
          if (a[param] < b[param]) {
            return 1
          } else if (a[param] > b[param]) {
            return -1
          } else {
            return 0
          }
        }),
        sort_key: param
      })
    }
  },

  onLoadMore: function() {
    this.setState({
      current_page: this.state.current_page + 1
    })
  },

  // Used in <Paginator /> (if we would use it)
  onChangePage: function(page) {
    this.setState({current_page: page});
    $.scrollTo('#fraction-filter-component', 100, {offset: -40})
  },

  selectFilter: function(option) {
    this.setState({filter_selected: option, current_page: 1})
  },

  render: function() {
    var sortkeys = this.props.keys,
        self = this,
        slice_from = 1,
        slice_to = this.state.current_page*this.state.items_per_page,
        current_page = this.state.current_page,
        elementListWidth = (this.props.sidebar_filter) ? 'fourteen' : 'sixteen',
        filtered_items = this.state.items,
        showSidebar;

    if (this.props.sidebar_filter) {
      showSidebar = (
        <SidebarFilter options={this.state.filter_options}
                       selected_filter={this.state.filter_selected}
                       callback={this.selectFilter} />
      )

      // Filter items to show only selected.
      if (this.state.filter_selected != 'all') {
        var filtered_items = this.state.items.filter((item) => {
          return item.fraction_slug === this.state.filter_selected
        })
      }
    } else {
      showSidebar = null;
    }
    var total_pages = Math.round((filtered_items.length / this.state.items_per_page)+0.5);

    return (
      <div>
        <div className="ui zero margin page grid sort-keys">
          {sortkeys.map(function(sortkey, index) {
            // Creating proper class for sort keys using Semantic UI framework.
            column_count = (index === 0) ? 'eight' : 'two';
            active = (self.state.sort_key === sortkey.key) ? 'active ' : '';
            class_name = active + column_count + ' wide center aligned column'

            return (
              <SortKeySelector params={sortkey}
                               class_name={class_name}
                               handler={self.sortElements(sortkey.key)} />
            )
          })}
        </div>

        <Loader loaded={this.state.loaded}>
          <div className="ui zero margin page grid">
            <div className={elementListWidth + ' wide zero paddings column'}>
              <ElementList items={filtered_items.slice(slice_from, slice_to)}
                           rowComponent={this.props.rowComponent} />
            </div>

            {showSidebar}

          </div>
        </Loader>

        <div className={((total_pages < 2 || current_page === total_pages) ? 'hidden ' : '') + 'ui zero margin center aligned load_more grid'}>
          <a onClick={this.onLoadMore}> Load more </a>
        </div>
      </div>
    );
  }
});

var SidebarFilter = React.createClass({
  setSelected: function(key) {
    this.props.callback(key);
  },

  render: function() {
    return (
      <div className="two wide column">
        <div className="ui sticky">
          <div className="sidebar">
            {Object.keys(this.props.options).map( (key) => {
              var selected = (this.props.selected_filter === key) ? 'selected' : '';

              if (this.props.options[key].logo_url) {
                if (this.props.options[key].logo_url === '/media/') {
                  var logo_url = '/static/img/fractions/fraction-default.png'
                } else {
                  var logo_url = this.props.options[key].logo_url
                }

                var item = (
                  <div>
                    <img src={logo_url} />
                    <div className="title"><h4>{this.props.options[key].name}</h4></div>
                  </div>
                )
              } else {
                var item = <h4>{this.props.options[key].name}</h4>
              }

              return (
                <a className={'item ' + selected} onClick={this.setSelected.bind(this, key)}>
                  {item}
                </a>
              )
            })}
          </div>
        </div>
      </div>
    )
  }
});

var SortKeySelector = React.createClass({
  render: function() {
    return (
      <div className={this.props.class_name}>
        <a onClick={this.props.handler}>
          {this.props.params.title}
        </a>
      </div>
    )
  }
});

var ElementList = React.createClass({
  render: function() {
    var self = this;
    return (
      <div className="filtered-elements">
        {self.props.items.map(function (item) {
          return (
              <self.props.rowComponent obj={item} />
          )
        })}
      </div>
    );
  }
});
