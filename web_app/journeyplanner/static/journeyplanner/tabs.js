/**
 * Defines the bootstrap tabs handler.
 *
 * @param {string} element
 *  Element.
 */
var tabsActions = function (element) {
    this.element = $(element);
  
    this.setup = function () {
      if (this.element.length <= 0) {
        return;
      }
      this.init();
      // Update after resize window.
      var resizeId = null;
      $(window).resize(function () {
        clearTimeout(resizeId);
        resizeId = setTimeout(() => {this.init()}, 50);
      }.bind(this));
    };
    
    this.init = function () {
   
      // Add class to overflow items.
      this.actionOverflowItems();
      var tabs_overflow = this.element.find('.overflow-tab');
   
      // Build overflow action tab element.
      if (tabs_overflow.length > 0) {
        if (!this.element.find('.overflow-tab-action').length) {
          var tab_link = $('<a>')
            .addClass('nav-link')
            .attr('href', '#')
            .attr('data-toggle', 'dropdown')
            .text('...')
            .on('click', function (e) {
              e.preventDefault();
              $(this).parents('.nav.nav-tabs').children('.nav-item.overflow-tab').toggle();
            });
  
          var overflow_tab_action = $('<li>')
            .addClass('nav-item')
            .addClass('overflow-tab-action')
            .append(tab_link);
  
          // Add hide to overflow tabs when click on any tab.
          this.element.find('.nav-link').on('click', function (e) {
            $(this).parents('.nav.nav-tabs').children('.nav-item.overflow-tab').hide();
          });
          this.element.append(overflow_tab_action);
        }
        
        this.openOverflowDropdown();
      }
      else {
        this.element.find('.overflow-tab-action').remove();
      }
   };
   
    this.openOverflowDropdown = function () {
      var overflow_sum_height = 0;
      var overflow_first_top = 41;
      
      this.element.find('.overflow-tab').hide();
      // Calc top position of overflow tabs.
      this.element.find('.overflow-tab').each(function () {
        var overflow_item_height = $(this).height() - 1;
        if (overflow_sum_height === 0) {
          $(this).css('top', overflow_first_top + 'px');
          overflow_sum_height += overflow_first_top + overflow_item_height;
        }
        else {
          $(this).css('top', overflow_sum_height + 'px');
          overflow_sum_height += overflow_item_height;
        }
  
      });
    };
  
    this.actionOverflowItems = function () {
      var tabs_limit = this.element.width() - 100;
      var count = 0;
      
      // Calc tans width and add class to any tab that is overflow.
      for (var i = 0; i < this.element.children().length; i += 1) {
        var item = $(this.element.children()[i]);
        if (item.hasClass('overflow-tab-action')) {
          continue;
        }
        
        count += item.width();
        if (count > tabs_limit) {
          item.addClass('overflow-tab');
        }
        else if (count < tabs_limit) {
          item.removeClass('overflow-tab');
          item.show();
        }
      }
    };
  };
  
  var tabsAction = new tabsActions('.layout--tabs .nav-tabs-wrapper .nav-tabs');
  tabsAction.setup();
  