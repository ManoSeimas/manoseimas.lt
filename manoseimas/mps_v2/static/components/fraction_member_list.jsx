var FractionMemberList = React.createClass({
    render: function() {
        var keys = [
          {key: 'last_name', title: 'Pavardė', icon: undefined, order: 1},
          {key: 'vote_percentage', title: 'Dalyvavimas balsavimuose', icon: '', order: -1},
          {key: 'statement_count', title: 'Aktyvumas diskusijose', icon: 'comment outline icon', order: -1},
          {key: 'passed_law_project_ratio', title: 'Projektų teikimo sėkmė', icon: '', order: -1}
        ];
        var default_key = 'last_name';
        var default_order = 1;
        return (
          <div className='ui zero margin page grid active_tab'>
            <SortableList endpoint={this.props.endpoint}
                          rowComponent={PaliamentarianRow}
                          keys={keys}
                          default_key={default_key}
                          default_order={default_order}
                          sidebar_filter={undefined} />
          </div>
        )
    }

});

var endpoint = $('#fraction-member-list').attr("data-endpoint");

React.render(
  <FractionMemberList endpoint={endpoint} />,
  document.getElementById('fraction-member-list')
);
