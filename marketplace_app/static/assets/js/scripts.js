'use strict';
(function($) {

    function getCookie(name) {
        // return cookie
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            let cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                let cookie = jQuery.trim(cookies[i]);
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function uuidv4() {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
            let r = Math.random() * 16 | 0,
                v = c === 'x' ? r : (r & 0x3 | 0x8);
            return v.toString(16);
        });
    }

    function eraseCookie(name) {
        document.cookie = `${name}=` + '' + '=; Max-Age=0'
    }

    // set device var
    let deviceCookie = 'device'
    let device = getCookie(deviceCookie)
    if (device === null || device === undefined) {
        device = uuidv4()
    }
    document.cookie = 'device=' + device + ";domain=;path=/"

    var px = ''; //'rt--'

    /**
     * Функция для вывода набора jQuery по селектору, к селектору добавляются
     * префиксы
     *
     * @param {string} selector Принимает селектор для формирования набора
     * @return {jQuery} Возвращает новый jQuery набор по выбранным селекторам
     */
    function $x(selector) {
        return $(x(selector));
    }

    /**
     * Функция для автоматического добавления префиксов к селекторы
     *
     * @param {string} selector Принимает селектор для формирования набора
     * @return {string} Возвращает новый jQuery набор по выбранным селекторам
     */
    function x(selector) {
        var arraySelectors = selector.split('.'),
            firstNotClass = !!arraySelectors[0];

        selector = '';

        for (var i = 0; i < arraySelectors.length; i++) {
            if (!i) {
                if (firstNotClass) selector += arraySelectors[i];
                continue;
            }
            selector += '.' + px + arraySelectors[i];
        }

        return selector;
    }

    // Прелоадер
    $(function() {

        var menu = function() {
            var $menuMain = $('.menu_main');
            $menuMain.css('position', 'absolute');
            var menuHeight = $('.menu_main').outerHeight();
            $menuMain.css('position', 'static');
            var $body = $('body');

            function refresh() {
                if (window.innerWidth < 991) {
                    // $('.menuModal').each(function(){
                    //     var $this = $(this);
                    //     setTimeout(function(){
                    //         if ($this.attr('height') > 0) {
                    //             $this.css('height', 0);
                    //         }
                    //     }, 100);
                    // });
                    $('.menuModal').css('height', 0);
                    $menuMain.css('position', 'absolute');
                    menuHeight = $('.menu_main').outerHeight();
                    $menuMain.css('position', 'static');
                } else {
                    menuHeight = $('.menu_main').outerHeight();
                    $('.menuModal')
                        .removeClass("menuModal_OPEN")
                        .css('height', '');
                    $body.removeClass("Site_menuOPEN");
                    $('.menuTrigger').removeClass("menuTrigger_OPEN");
                }
            }

            return {
                init: function() {
                    if (window.innerWidth < 991) {
                        $(".menuModal").css('height', menuHeight);
                        // Меню для мобильных
                        $(".menuTrigger").each(function() {
                            $($(this).attr('href')).css('height', 0);
                        });
                    }

                    $(".menuTrigger").click(function(e) {
                        var $this = $(this),
                            href = $this.attr("href");

                        if ($this.hasClass("menuTrigger_OPEN")) {
                            $body.removeClass("Site_menuOPEN");
                            $(href)
                                .removeClass("menuModal_OPEN")
                                .css('height', 0);
                            $this.removeClass("menuTrigger_OPEN");
                        } else {
                            $body.addClass("Site_menuOPEN");
                            $(href)
                                .addClass("menuModal_OPEN")
                                .css('height', menuHeight);
                            $this.addClass("menuTrigger_OPEN");
                        }
                        e.preventDefault();
                    });
                    $(window).on('resize', refresh);
                }
            };
        };
        menu().init();
        var search = function() {
            var $searchLink = $('.Header-searchLink');
            return {
                init: function() {
                    $searchLink.each(function() {
                        var $this = $(this);
                        $this.on('click', function() {
                            var $thisClick = $(this);
                            $thisClick.next('.Header-search').toggleClass('Header-search_open');
                        });
                    });
                }
            };
        };
        search().init();
        var form = function() {
            var $selectList = $('.selectList');
            var $input = $('.form-input, .form-textarea');
            var $form = $('.form');
            var $select = $('.form-select');
            return {
                init: function() {
                    $selectList.each(function() {
                        var $this = $(this),
                            $radio = $this.find('input[type="radio"]');

                        function changeTitle($block, $element) {
                            $block.find('.selectList-title')
                                .text($element.closest('.selectList-item')
                                    .find('.selectList-text').text())
                        }

                        changeTitle($this, $radio.filter('[checked="checked"]'));
                        $radio.on('change', function() {
                            changeTitle($this, $(this));
                        });

                    });
                    $(document).on('click', function(e) {
                        var $this = $(e.target);
                        if (!$this.hasClass('selectList-header')) {
                            $this = $(e.target).closest('.selectList-header');
                        }
                        if ($this.length) {
                            e.preventDefault();
                            $this.closest('.selectList').toggleClass('selectList_OPEN');
                        } else {
                            $('.selectList').removeClass('selectList_OPEN');
                        }
                    });

                    // Валидация полей
                    $input.on('blur', function() {
                        var $this = $(this),
                            validate = $this.data('validate'),
                            message = '',
                            error = false;
                        if (validate) {
                            validate = validate.split(' ');
                            validate.forEach(function(v) {
                                switch (v) {
                                    case 'require':
                                        if (!$this.val()) {
                                            message = 'Это поле обязательно для заполнения. ';
                                            error = true;
                                        }
                                        break;
                                    case 'pay':
                                        var val = $this.val().replace(' ', '');
                                        val = val + '';
                                        if (parseFloat(val) % 2 !== 0) {
                                            message += 'Номер должен быть четным. ';
                                            error = true;
                                        }
                                        break;

                                }
                                if (error) {
                                    if ($this.hasClass('form-input')) {
                                        $this.addClass('form-input_error');
                                    }
                                    if ($this.hasClass('form-textarea')) {
                                        $this.addClass('form-textarea_error');
                                    }
                                    if (!$this.next('.form-error').length) {
                                        $this.after('<div class="form-error">' + message + '</div>');
                                    }
                                    $this.data('errorinput', true);
                                } else {
                                    $this.next('.form-error').remove();
                                    $this.removeClass('form-input_error');
                                    $this.removeClass('form-textarea_error');
                                    $this.data('errorinput', false);
                                }
                                message = '';

                            });
                        }

                    });
                    $form.on('submit', function(e) {
                        var $this = $(this),
                            $validate = $this.find('[data-validate]');

                        $validate.each(function() {
                            var $this = $(this);
                            $this.trigger('blur');
                            if ($this.data('errorinput')) {
                                e.preventDefault();
                            }
                        });
                    });
                    $select.wrap('<div class="form-selectWrap"></div>');
                    $('[data-mask]').each(function() {
                        var $this = $(this);
                        $this.mask($this.data('mask'), {
                            placeholder: 'x'
                        });
                    });
                }
            };
        };
        form().init();
        let modal = function() {
            let $trigger = $('.trigger'),
                $body = $('body'),
                $modal = $('.modal');

            let template = {
                img: (img) => '<div class="modal">' +
                    '<div class="modal-window">' +
                    '<a href="#" class="modal-close fa fa-close"></a>' +
                    '<img src="' + img + '" />' +
                    '</div>' +
                    '</div>'
            };

            return {
                refresh: function() {},
                init: function() {
                    function modalClick(e) {

                        let $target = $(e.target),
                            $this = $(this);

                        if ($target.hasClass('modal-close')) {
                            $target = $this;
                        }

                        if ($this.is($target)) {
                            e.preventDefault();
                            $body.removeClass("Site_modalOPEN");
                            $this.removeClass("modal_OPEN");
                            $('[href="' + $this.attr('id') + '"]').removeClass("trigger_OPEN");
                        }
                    }

                    $trigger.click(function(e) {
                        e.preventDefault();

                        let $this = $(this),
                            href = $this.attr("href"),
                            $href = $(href);

                        if (!$(href).length) {
                            let $img = $(template.img($this.data('src')));
                            $img.attr('id', href.replace('#', ''));
                            $body.append($img);
                            $href = $(href);
                            $modal = $modal.add($href);
                            $href.click(modalClick);
                        }

                        $href.addClass("modal_OPEN");
                        $body.addClass("Site_modalOPEN");
                        $this.addClass("trigger_OPEN");
                    });

                    $modal.click(modalClick);

                }
            };
        };

        modal().init();
        var range = function() {
            return {
                init: function() {
                    var $range = $('.range'),
                        $line = $range.find('.range-line');

                    $line.ionRangeSlider({
                        onStart: function(data) {
                            $('.rangePrice').text(
                                '$' + data.from + ' - $' + data.to
                            )
                        },
                        onChange: function(data) {
                            $('.rangePrice').text(
                                '$' + data.from + ' - $' + data.to
                            )
                        }
                    });
                }
            };
        };
        range().init();
        var table = function() {
            return {
                init: function() {}
            };
        };
        table().init();
        //END
        var PanelAdd = function() {
            return {
                init: function() {}
            };
        };
        PanelAdd().init();
        var ControlPanel = function() {
            return {
                init: function() {}
            };
        };
        ControlPanel().init();
        var Slider = function() {
            let $block = $('.Slider').not('.Slider_carousel'),
                $container = $block.children('.Slider-box'),
                $carousel = $('.Slider_carousel'),
                $containerCar = $carousel.children('.Slider-box');
            return {
                init: function() {
                    $container.each(function() {
                        var $this = $(this);
                        var $navigate = $this.closest($block).find('.Slider-navigate');
                        $this.slick({
                            dots: true,
                            arrows: true,
                            autoplay: true,
                            appendArrows: $navigate,
                            appendDots: $navigate,
                            autoplaySpeed: 3000
                        });
                    });
                    $containerCar.each(function() {
                        var $this = $(this);
                        var $navigate = $this.closest($carousel).find('.Slider-navigate');
                        if ($this.hasClass('Cards_hz')) {
                            $this.slick({
                                appendArrows: $navigate,
                                appendDots: $navigate,
                                dots: true,
                                arrows: true,
                                slidesToShow: 3,
                                slidesToScroll: 2,
                                responsive: [{
                                        breakpoint: 1600,
                                        settings: {
                                            slidesToShow: 2,
                                            slidesToScroll: 2
                                        }
                                    },
                                    {
                                        breakpoint: 900,
                                        settings: {
                                            slidesToShow: 1,
                                            slidesToScroll: 1
                                        }
                                    }
                                ]
                            });

                        } else {
                            $this.slick({
                                appendArrows: $navigate,
                                appendDots: $navigate,
                                dots: true,
                                arrows: true,
                                slidesToShow: 4,
                                slidesToScroll: 2,
                                responsive: [{
                                        breakpoint: 1600,
                                        settings: {
                                            slidesToShow: 3,
                                            slidesToScroll: 2
                                        }
                                    },
                                    {
                                        breakpoint: 1230,
                                        settings: {
                                            slidesToShow: 2,
                                            slidesToScroll: 2
                                        }
                                    },
                                    {
                                        breakpoint: 570,
                                        settings: {
                                            slidesToShow: 1,
                                            slidesToScroll: 1
                                        }
                                    }
                                ]
                            });

                        }
                    });

                }
            };
        };
        Slider().init();
        var CartBlock = function() {
            return {
                init: function() {}
            };
        };
        CartBlock().init();
        var CategoriesButton = function() {
            return {
                init: function() {
                    $(document).on('click', function(e) {
                        var $this = $(e.target);
                        if ($this.is('a.CategoriesButton-arrow') && $this.closest('.CategoriesButton-link').length) {
                            e.preventDefault();
                            if ($this.next('.CategoriesButton-submenu').is(':visible')) {
                                $('.CategoriesButton .CategoriesButton-submenu').hide(0);
                            } else {
                                $('.CategoriesButton .CategoriesButton-submenu').hide(0);
                                $this.next('.CategoriesButton-submenu').show(0);
                            }
                        } else {
                            if (!$this.hasClass('CategoriesButton-title')) {
                                $this = $(e.target).closest('.CategoriesButton-title');
                            }
                            if ($this.length) {
                                e.preventDefault();
                                $this.closest('.CategoriesButton').toggleClass('CategoriesButton_OPEN');
                            } else {
                                $('.CategoriesButton').removeClass('CategoriesButton_OPEN');
                                $('.CategoriesButton .CategoriesButton-submenu').hide(0);
                            }
                        }
                    });
                }
            };
        };
        CategoriesButton().init();
        var Middle = function() {
            return {
                init: function() {}
            };
        };
        Middle().init();
        var Section = function() {
            return {
                init: function() {}
            };
        };
        Section().init();
        var BannersHome = function() {
            return {
                init: function() {}
            };
        };
        BannersHome().init();
        var Card = function() {
            return {
                init: function() {}
            };
        };
        Card().init();
        var CountDown = function() {
            var $blocks = $('.CountDown');

            function getTimeRemaining(endtime) {
                endtime = endtime.split(' ');
                var date = endtime[0].split('.');
                var time = endtime[1].split(':');
                var t = new Date(date[2], date[1] - 1, date[0], time[0], time[1]) - new Date();
                var seconds = Math.floor((t / 1000) % 60);
                var minutes = Math.floor((t / 1000 / 60) % 60);
                var hours = Math.floor((t / (1000 * 60 * 60)) % 24);
                var days = Math.floor(t / (1000 * 60 * 60 * 24));
                return {
                    'total': t,
                    'days': days,
                    'hours': hours,
                    'minutes': minutes,
                    'seconds': seconds
                };
            }

            function initializeClock(clock, endtime) {
                function updateClock() {
                    var t = getTimeRemaining(endtime);
                    clock.find('.CountDown-days').text(t.days);
                    clock.find('.CountDown-hours').text(t.hours);
                    clock.find('.CountDown-minutes').text(t.minutes);
                    clock.find('.CountDown-secs').text(t.seconds);
                    if (t.total <= 0) {
                        clearInterval(timeinterval);
                    }
                }

                updateClock();
                var timeinterval = setInterval(updateClock, 1000);
            }

            return {
                init: function() {
                    $blocks.each(function() {
                        var $this = $(this);
                        initializeClock($this, $this.data('date'));
                    });
                }
            };
        };
        CountDown().init();
        var Rating = function() {
            return {
                init: function() {
                    $('.Rating_input:not(.Rating_inputClick)').on('click', function() {
                        $(this).addClass('Rating_inputClick');
                    });
                }
            };
        };
        Rating().init();
        var Choice = function() {
            return {
                init: function() {}
            };
        };
        Choice().init();
        var Map = function() {
            return {
                init: function() {}
            };
        };
        Map().init();
        var Pagination = function() {
            return {
                init: function() {}
            };
        };
        Pagination().init();
        var Sort = function() {
            return {
                init: function() {}
            };
        };
        Sort().init();
        var Compare = function() {
            var $compare = $('.Compare');
            var $products = $compare.find('.Compare-products');
            var $checkDifferent = $('.Compare-checkDifferent input');
            return {
                init: function() {
                    $products.on('scroll', function() {
                        var $this = $(this);
                        $products.each(function() {
                            $(this)[0].scrollLeft = $this[0].scrollLeft;
                        })
                    });
                    $checkDifferent.on('change', function() {
                        var $this = $(this),
                            $rowsHide = $this.closest($compare).find('.Compare-row_hide');
                        if ($this.prop('checked')) {
                            $rowsHide.hide(0);
                        } else {
                            $rowsHide.show(0);
                        }
                    });
                    $checkDifferent.trigger('change');
                }
            };
        };
        Compare().init();
        var Sort = function() {
            return {
                init: function() {}
            };
        };
        Sort().init();
        var NavigateProfile = function() {
            return {
                init: function() {}
            };
        };
        NavigateProfile().init();
        var Profile = function() {
            var $avatar = $('.Profile-avatar');
            return {
                init: function() {
                    var $avatarfile = $avatar.find('.Profile-file');

                    function readURL(input) {
                        if (input.files && input.files[0]) {
                            var file = input.files[0],
                                ext = 'неизвестно';
                            ext = file.name.split('.').pop();
                            if (ext === 'png' || ext === 'jpg' || ext === 'gif') {
                                var reader = new FileReader();

                                reader.onload = function(e) {
                                    $(input).closest($avatar).find('.Profile-img img').attr('src', e.target.result);
                                }

                                reader.readAsDataURL(file);
                                return true;
                            }
                            return false;
                        }
                    }

                    $avatarfile.change(function() {
                        var $thisAvatar = $(this).closest($avatar);
                        if (readURL(this)) {
                            $thisAvatar.removeClass('Profile-avatar_noimg');
                            $thisAvatar.next('.form-error').remove();
                            $thisAvatar.find('input[type="file"]').data('errorinput', false);
                        } else {
                            if (!$thisAvatar.next('.form-error').length) {
                                $thisAvatar.find('input[type="file"]').data('errorinput', true);
                                $thisAvatar.after('<div class="form-error">Для загрузки допустимы лишь картинки с расширением png, jpg, gif</div>');
                            }
                        };
                    });
                }
            };
        };
        Profile().init();
        var Cart = function() {
            return {
                init: function() {}
            };
        };
        Cart().init();
        var Amount = function() {
            var $amount = $('.Amount');
            var $add = $('.Amount-add');
            var $input = $('.Amount-input');
            var $remove = $('.Amount-remove');
            return {
                init: function() {
                    $add.on('click', function(e) {
                        e.preventDefault();
                        var $inputThis = $(this).siblings($input).filter($input);
                        var value = parseFloat($inputThis.val());
                        $inputThis.val(value + 1)
                    });
                    $remove.on('click', function(e) {
                        e.preventDefault();
                        var $inputThis = $(this).siblings($input).filter($input);
                        var value = parseFloat($inputThis.val());
                        $inputThis.val(value > 0 ? value - 1 : 0);
                    });
                }
            };
        };
        Amount().init();

        $(document).on('click', '.order-navigate-link', function(event) {
            event.preventDefault();
            const target = event.currentTarget
            let data = {}
            let stepName = target.href.substring(target.href.lastIndexOf('/') + 1)
            if (stepName !== "#") {
                data['wizard_goto_step'] = stepName
                $.ajax({
                    type: 'POST',
                    beforeSend: setCSRFHeader,
                    url: target.baseURI,
                    data: data,
                    success: function(response) {
                        document.body.innerHTML = response
                    },
                    error: function(xhr, errmsg, err) {}
                });
            }

        })

        $(document).ready(function() {
            let orderStep = document.getElementById('order-step')
            let navigateMenu = document.querySelector('.Order-navigate')
            let navigateItem = document.querySelectorAll('.menu-item')
            navigateItem.forEach((item) => {
                if (navigateMenu) {
                    if (navigateMenu.contains(item)) {
                        if (parseInt(item.value) === parseInt(orderStep.value)) {
                            item.classList.add('menu-item_ACTIVE')
                            item.classList.remove('menu-item_COMPLETE')
                        } else if (parseInt(item.value) < parseInt(orderStep.value)) {
                            item.classList.remove('menu-item_ACTIVE')
                            item.classList.add('menu-item_COMPLETE')
                        } else {
                            item.classList.remove('menu-item_ACTIVE')
                            item.classList.remove('menu-item_COMPLETE')
                            let anchor = item.getElementsByTagName('a')[0]
                            anchor.setAttribute('href', '#')
                        }
                    }
                }
            })
        })


        $(document).on('click', '.order-prev-step', function(event) {
            event.preventDefault();
            const target = event.currentTarget;
            let prevStepButtons = document.querySelectorAll('.order-prev-step')
            if (target) {
                prevStepButtons.forEach((item) => {
                    if (item === target) {
                        let data = {}
                        data[item.name] = item.value
                        $.ajax({
                            type: 'POST',
                            beforeSend: setCSRFHeader,
                            url: target.href,
                            data: data,
                            success: function(response) {
                                document.body.innerHTML = response
                            },
                            error: function(xhr, errmsg, err) {}
                        });
                    }
                })
            }

        })

        var Account = function() {
            return {
                init: function() {}
            };
        };
        Account().init();
        var Payment = function() {
            return {
                init: function() {
                    $('.Payment-generate').on('click', function(e) {
                        var $this = $(this),
                            $bill = $this.closest('.Payment').find('.Payment-bill'),
                            billNumber = '';
                        e.preventDefault();
                        do {
                            billNumber = Math.random() + '';
                            billNumber = billNumber.slice(-9, -1);
                        } while (parseFloat(billNumber) % 2 !== 0);
                        billNumber = billNumber.slice(0, 4) + ' ' + billNumber.slice(4, 8);
                        $bill.val(billNumber);
                    });
                    $('.Payment-pay .btn').on('click', function(e) {
                        var $this = $(this),
                            $validate = $this.closest('.form').find('[data-validate]');

                        $validate.each(function() {
                            var $this = $(this);
                            $this.trigger('blur');
                            if ($this.data('errorinput')) {
                                e.preventDefault();
                            }
                        });
                    });
                }
            };
        };
        Payment().init();
        var Tabs = function() {
            var $tabs = $('.Tabs');
            var $tabsLink = $('.Tabs-link');
            var $tabsBlock = $('.Tabs-block');
            return {
                init: function() {
                    // var $steps = $('.Tabs_steps');
                    // var $step = $steps.find($tabsLink).not($steps.find($tabs).find($tabsLink));
                    // var $blocks = $steps.find($tabsBlock).not($steps.find($tabs).find($tabsBlock));
                    // $blocks.hide(0);
                    // var href = $step.eq(0).attr('href');
                    // var $active = $(href);
                    // var $links= $step.add($step.siblings($tabsLink));
                    // $links.removeClass('Tabs-link_ACTIVE');
                    // $step.eq(0).addClass('Tabs-link_ACTIVE');
                    // $active.show(0);

                    $tabsLink.on('click', function(e) {
                        var $this = $(this);
                        var href = $this.attr('href');
                        if (href[0] === "#") {
                            e.preventDefault();
                            var $parent = $this.closest($tabs);
                            if ($parent.hasClass('Tabs_steps')) {} else {
                                var $blocks = $parent.find($tabsBlock).not($parent.find($tabs).find($tabsBlock));
                                var $links = $this.add($this.siblings($tabsLink));
                                var $active = $(href);
                                $links.removeClass('Tabs-link_ACTIVE');
                                $this.addClass('Tabs-link_ACTIVE');
                                $blocks.hide(0);
                                $active.show(0);
                            }
                        }

                    });
                    $('.TabsLink').on('click', function(e) {
                        var $this = $(this);
                        var href = $this.attr('href');
                        var $active = $(href);
                        var $parent = $active.closest($tabs);
                        if ($parent.hasClass('Tabs_steps')) {} else {
                            var $blocks = $parent.find($tabsBlock).not($parent.find($tabs).find($tabsBlock));
                            var $link = $('.Tabs-link[href="' + href + '"]');
                            var $links = $link.add($link.siblings($tabsLink));
                            $links.removeClass('Tabs-link_ACTIVE');
                            $link.addClass('Tabs-link_ACTIVE');
                            $blocks.hide(0);
                            $active.show(0);
                        }

                    });
                    $tabs.each(function() {
                        $(this).find($tabsLink).eq(0).trigger('click');
                    });
                }
            };
        };
        Tabs().init();
        // setTimeout(function(){
        //     $('body').css('opacity', '1');
        // }, 100);
        var ProductCard = function() {
            var $picts = $('.ProductCard-pict');
            var $photo = $('.ProductCard-photo');
            return {
                init: function() {
                    $picts.on('click', function(e) {
                        e.preventDefault();
                        var $this = $(this);
                        var href = $this.attr('href');
                        $photo.empty();
                        $photo.append('<img src="' + href + '" />');
                        $picts.removeClass('ProductCard-pict_ACTIVE');
                        $this.addClass('ProductCard-pict_ACTIVE');
                    });
                }
            };
        };
        ProductCard().init();
        var Comments = function() {
            return {
                init: function() {
                    $('[data-action="comments-show"]').on('click', function(e) {
                        e.preventDefault();
                        var $this = $(this),
                            text = $this.data('text-alt'),
                            $comments = $this.prev('.Comments').find('.Comments-wrap_toggle');
                        $this.data('text-alt', $this.text());
                        $this.text(text);
                        $comments
                            .toggleClass('Comments-wrap_HIDE');
                        $('.fixScrollBlock').trigger('render.airStickyBlock');
                    });
                }
            };
        };
        Comments().init();
        var Product = function() {
            return {
                init: function() {}
            };
        };
        Product().init();
        var ProgressPayment = function() {
            return {
                init: function() {}
            };
        };
        ProgressPayment().init();
        var Categories = function() {
            return {
                init: function() {
                    if ($(window).width() < 990) {
                        var $more = $('.Categories-more'),
                            $trigger = $('.Categories-trigger');
                        $trigger.on('click', function(e) {
                            e.preventDefault();
                            var $this = $(this),
                                text = $this.data('text-alt'),
                                $block = $this.prev($more);
                            $this.data('text-alt', $this.text());
                            $this.text(text);
                            $this.toggleClass('Categories-trigger_OPEN');
                            $block.toggle(0);
                        });
                    }
                }
            };
        };
        Categories().init();
    });

    // call pop with text
    function popUp(message, type) {
        return alertify.notify(message, type)
    }

    // set value for input
    function setInputValue(item, value) {
        let idValue = 'inputValueToChange'
        item.setAttribute('id', idValue)
        document.getElementById(idValue).value = value
        item.removeAttribute('id')
    }

    function setCSRFHeader(xhr) {
        xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
    }

    // get click-events on all objects with add-to-cart id
    // add product to cart
    $(document).on('click', '#add-to-cart', function(event) {
        let addToCardButtons = document.querySelectorAll('.Card-btn, .Compare-btn, .Product-btn, .add_to_cart_shop');
        event.preventDefault();
        const target = event.currentTarget;
        let is_product = false
        if (target && target.classList.contains('product')) {
            is_product = true
            addToCardButtons.forEach((item) => {
                if (target === item) {
                    $.ajax({
                        type: 'POST',
                        beforeSend: setCSRFHeader,
                        url: target.href,
                        data: {
                            'is_product': is_product,
                            'method': 'post'
                        },
                        success: function(response) {
                            document.getElementById("CartBlock-amount").innerHTML = response.cart_count
                            document.getElementById("CartBlock-price").innerHTML = response.price
                            popUp(response.message, response.type);
                        },
                        error: function(xhr, errmsg, err) {
                            popUp(err, 'error');

                        }
                    });
                }
            });
        }
    });


    // get click-events on all objects with add-to-cart id
    // add product to cart
    $(document).on('click', '#add-to-cart-shop', function(event) {
        let addToCardButtons = document.querySelectorAll('.add_to_cart_shop');
        event.preventDefault();
        const target = event.currentTarget;
        let is_product = false
        if (target && target.classList.contains('product')) {
            is_product = true
            addToCardButtons.forEach((item) => {
                if (target === item) {
                    $.ajax({
                        type: 'POST',
                        beforeSend: setCSRFHeader,
                        url: target.href,
                        data: {
                            'is_product': is_product,
                            'method': 'post'
                        },
                        success: function(response) {
                            document.getElementById("CartBlock-amount").innerHTML = response.cart_count
                            document.getElementById("CartBlock-price").innerHTML = response.price
                            popUp(response.message, response.type);
                        },
                        error: function(xhr, errmsg, err) {
                            popUp(err, 'error');

                        }
                    });
                }
            });
        }
    });

    // get click-events on all objects with add-to-cart id
    // add product to cart
    $(document).on('click', '#add-to-cart', function(event) {
        let addToCardButtons = document.querySelectorAll('.add_to_cart');
        event.preventDefault();
        const target = event.currentTarget;
        let is_product = false
        if (target && target.classList.contains('product')) {
            is_product = true
            let cnt = document.getElementsByName("amount")
            addToCardButtons.forEach((item) => {
                if (target === item) {
                    $.ajax({
                        type: 'POST',
                        beforeSend: setCSRFHeader,
                        url: target.href + '/' + cnt[0].value,
                        data: {
                            'is_product': is_product,
                            'method': 'post'
                        },
                        success: function(response) {
                            document.getElementById("CartBlock-amount").innerHTML = response.cart_count
                            document.getElementById("CartBlock-price").innerHTML = response.price
                            popUp(response.message, response.type);
                        },
                        error: function(xhr, errmsg, err) {
                            popUp(err, 'error');

                        }
                    });
                }
            });
        }
    });

    // get quantity block text
    function getQuantityFromParentNode(element) {
        let quantityClass = '.Cart-quantity'
        let parentClass = '.Cart-product'
        let quantityText = null
        let parentNodes = document.querySelectorAll(parentClass)
        parentNodes.forEach((item) => {
            if (item.contains(element)) {
                quantityText = item.querySelector(quantityClass).textContent
                return quantityText
            }
        })
        return quantityText
    }


    // get click-events on all objects with Cart-delete class
    // delete product from cart
    $(document).on('click', '.Cart-delete', function(event) {
        let deleteButtons = document.querySelectorAll('.Cart-delete');
        event.preventDefault();
        const target = event.currentTarget;
        if (target) {
            deleteButtons.forEach((item) => {
                if (target === item) {
                    $.ajax({
                        type: 'DELETE',
                        beforeSend: setCSRFHeader,
                        url: target.href,
                        data: {
                            'method': 'delete'
                        },
                        success: function(response) {
                            popUp(response.message, response.type);
                            setTimeout(() => window.location.reload(), 1000);
                        },
                        error: function(xhr, errmsg, err) {
                            popUp(err, 'error');
                        }
                    });
                }
            });
        }
    });

    // get click-events on all objects with Cart-block_seller class
    // change product's shop
    $('.Cart-block_seller').on('change', function(event) {
        let shopOptions = document.querySelectorAll('.Cart-block_seller');
        event.preventDefault();
        const target = event.currentTarget;
        if (target) {
            shopOptions.forEach((item) => {
                if (target === item) {
                    let shopId = $(target).find('option:selected').attr('value');
                    let stockId = target.parentNode.querySelector('.Amount-remove').value;
                    $.ajax({
                        type: 'POST',
                        beforeSend: setCSRFHeader,
                        url: target.href,
                        data: {
                            'stock_id': stockId,
                            'shop_id': shopId,
                            'method': 'post'
                        },
                        success: function(response) {
                            popUp(response.message, response.type);
                            setTimeout(() => window.location.reload(), 2000);
                        },
                        error: function(xhr, errmsg, err) {
                            popUp(err, 'error');
                        }
                    });
                }
            })
        }
    });

    // get click-events on all objects with add-to-compare id
    // add product to compare
    $(document).on('click', '#add-to-compare', function(event) {
        let addToCardButtons = document.querySelectorAll('.Card-btn, .btn_default');
        event.preventDefault();
        const target = event.currentTarget;
        let is_product = false
        if (target && target.classList.contains('product')) {
            is_product = true
            addToCardButtons.forEach((item) => {
                if (target === item) {
                    $.ajax({
                        type: 'POST',
                        url: target.href,
                        data: {
                            'is_product': is_product,
                            'csrfmiddlewaretoken': getCookie('csrftoken'),
                            'method': 'post'
                        },
                        success: function(response) {
                            document.getElementById("Compare-amount").innerHTML = response.head_count,
                                popUp(response.message, response.type);
                        },
                        error: function(xhr, errmsg, err) {
                            popUp(err, 'error');

                        }
                    });
                }
            });
        }
    });

    // get click-events on all objects with Compare-delete class
    // delete product from compare
    $(document).on('click', '#delete-from-compare', function(event) {
        let deleteButtons = document.querySelectorAll('.Compare-delete');
        event.preventDefault();
        const target = event.currentTarget;
        if (target) {
            deleteButtons.forEach((item) => {
                if (target === item) {
                    $.ajax({
                        type: 'DELETE',
                        beforeSend: function(xhr) {
                            xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
                            xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
                        },
                        url: target.href,
                        data: {
                            'method': 'delete'
                        },
                        success: function(response) {
                            popUp(response.message, response.type);
                            setTimeout(() => window.location.reload(), 1000);
                        },
                        error: function(xhr, errmsg, err) {
                            popUp(err, 'error');
                        }
                    });
                }
            });
        }
    });

    // get click-events on all objects with add-to-view id
    // add product to view
    $(document).on('click', '#add-to-view', function(event) {
        let addToCardButtons = document.querySelectorAll('.Card-btn');
        event.preventDefault();
        const target = event.currentTarget;
        let is_product = false
        if (target && target.classList.contains('product')) {
            is_product = true
            addToCardButtons.forEach((item) => {
                if (target === item) {
                    $.ajax({
                        type: 'POST',
                        url: target.href,
                        data: {
                            'is_product': is_product,
                            'csrfmiddlewaretoken': getCookie('csrftoken'),
                            'method': 'post'
                        },
                        success: function(response) {
                            popUp(response.message, response.type);
                        },
                        error: function(xhr, errmsg, err) {
                            popUp(err, 'error');

                        }
                    });
                }
            });
        }
    });


    // clean cookie after logout
    $(document).on('click', '#logout-btn', function(event) {
        const target = event.currentTarget;
        eraseCookie(deviceCookie)
        $.ajax({
            type: 'POST',
            beforeSend: function(xhr) {
                xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
                xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
            },
            url: target.href,
            data: {
                'method': 'post'
            },
            success: function(response) {
                document.body.innerHTML = response
            },
            error: function(xhr, errmsg, err) {
                popUp(err, 'error');
            }
        });

    })

})(jQuery);