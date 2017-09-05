function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function getQueryParamByName(name, url) {
    if (!url) url = window.location.href;
    name = name.replace(/[\[\]]/g, "\\$&");
    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, " "));
}

function clearForm(formId) {
    $(':input','#' + formId)
      .not(':button, :submit, :reset, :hidden')
      .val('')
      .removeAttr('checked')
      .removeAttr('selected');
}

/**
 * @return function to load tweets which takes arguments: reload(boolean), query(string)
 */
function getLoadTweets(initialUrl) {
    var tweetsUrl = initialUrl;

    return function (reload, query) {
        var queryPrefix;
        if (reload) {
            queryPrefix = '?';
            tweetsUrl = initialUrl; // reset it
        } else queryPrefix = '&';

        var queryStr = '';
        if (query) queryStr = queryPrefix + 'q=' + query;

        $.ajax({
            'url': tweetsUrl + queryStr,
            'method': 'GET',
            'success': function (data) {
                tweetsUrl = data.next;
                var tweets = data.results;
                // toggle load more link
                if (!tweetsUrl || tweets.length == data.count) $('#loadMore').css('display', 'none');
                else $('#loadMore').css('display', '');

                clearForm('tweet-form');
                if (reload) $('#tweet-container').empty();
                $.each(tweets, function (key, tweet) {
                    var tweetContent = tweet.content.replace(/(?:\r\n|\r|\n)/g, '<br />'); // replace all "\n"s with "<br />"s
                    var tweetUser = tweet.user;

                    // don't show current user's name as a link
                    var userLink;
                    if (tweetUser.url.endsWith(currentUserName + "/")) {  // TOREFACTOR the tailing slash can be problematic
                        userLink = tweetUser.username;
                    } else {
                        userLink = "<a href='" + tweetUser.url + "'>" + tweetUser.username + "</a>";
                    }

                    $('#tweet-container').append(
                        "<div class=\"media\">" +
                            "<div class=\"media-body\">" +
                                tweetContent + "<br />" +
                                "via <b>" + userLink + "</b> | " + tweet.time_since + " ago" +
                                "<a class='btn btn-default view' href='" + tweet.url + "'>View</a>" + "<br />" +
                            "</div>" +
                        "</div>" +
                        "<hr />"
                    );
                });

                if ($('#tweet-container').children().length == 0) {
                    var query = getQueryParamByName('q');
                    if (query) {
                        $('#tweet-container').append('<div>No result!</div>');
                    } else {
                        $('#tweet-container').append('<div>No tweets yet!</div>');
                    }
                }
            },
            'error': function (data) {
                console.log('error:');
                console.log(data);
            }
        });
    };
}

function toggleFollow(requestUrl) {
    $.ajax({
        'url': requestUrl,
        'success': function (data) {
            var toggle = $('.follow-toggle[username=' + data.username + ']');
            if (data.is_following) toggle.text('unfollow');
            else toggle.text('follow');

            // refresh followed-by div
            $('#followed-by').empty();
            $.each(data.followed_by, function (index, user) {
                $('#followed-by').append('<a class="btn btn-link" href="' + user.url + '">' + user.username + '</a><br />');
            });
            if ($('#followed-by').children().length == 0) {
                $('#followed-by').append('<span class="info">Not followed by any users.</span>');
            }

            // update followed-by count
            $('.followed-by-count[username=' + data.username + ']').text(data.followed_by.length);

            // update following count
            var followingCountSpan = $('.following-count[username=' + currentUserName + ']');
            var followingCount = Number(followingCountSpan.text());
            if (data.is_following) followingCountSpan.text(followingCount + 1);
            else followingCountSpan.text(followingCount - 1);
        },
        'error': function (data) {
            console.log('error:');
            console.log(data);
        }
    });
}

/**
 * change color and the count number of how many chars left
 * color: chars left < 0 -> red
 *                   = 0 -> gray
 *                   > 0 -> black(original color)
 */
function setUpTweetCharsLeft(textArea) {
    var content = textArea.val();
    var charCountLeft = tweetCharsLimit - content.length;
    var charsLeftSpan = $('#tweetCharsLeft');
    charsLeftSpan.text(charCountLeft);
    if (charCountLeft == 0) {
        charsLeftSpan.removeClass('red-color');
        charsLeftSpan.addClass('grey-color');
    } else if (charCountLeft < 0) {
        charsLeftSpan.removeClass('grey-color');
        charsLeftSpan.addClass('red-color');
    } else {
        charsLeftSpan.removeClass('grey-color');
        charsLeftSpan.removeClass('red-color');
    }
}

/**
 * for tweet chars left and cmd + enter submission
 */
function initTweetForm() {
    // tweet chars left
    var tweetForm = $('#tweet-form');
    var textArea = $(tweetForm.find('textarea')[0]);
    setUpTweetCharsLeft(textArea);
    textArea.keyup(function (event) {
        setUpTweetCharsLeft(textArea);
    });

    // cmd + enter submission feature
    var cmdPressed;
    textArea.keydown(function (event) {
        if (event.which == 91 || event.which == 93) {  // key code 91 and 93: left and right "cmd"
            cmdPressed = true;
            setTimeout(function () {
                cmdPressed = false;
            }, 200);
        }
        if (cmdPressed && event.which == 13) {  // key code 13: "enter"
            tweetForm.submit();
        }
    });
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
