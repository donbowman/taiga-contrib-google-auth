angular.module("templates").run(["$templateCache", function($templateCache) {$templateCache.put("/plugins/google-auth/google-auth.html","\n<div tg-google-login-button=\"tg-google-login-button\"><a href=\"\" title=\"Enter with your google account\" class=\"button button-auth\"><img src=\"/plugins/google-auth/images/google-logo.png\" alt=\"\"/><span>Sign in with Google</span></a></div>");}]);

/*
 * Copyright (C) 2018 Don Bowman <db@donbowman.ca>
 * Copyright (C) 2014-2016 Andrey Antukh <niwi@niwi.nz>
 * Copyright (C) 2014-2016 Jesús Espino Garcia <jespinog@gmail.com>
 * Copyright (C) 2014-2016 David Barragán Merino <bameda@dbarragan.com>
 * Copyright (C) 2014-2016 Alejandro Alonso <alejandro.alonso@kaleidos.net>
 * Copyright (C) 2014-2016 Juan Francisco Alcántara <juanfran.alcantara@kaleidos.net>
 * Copyright (C) 2014-2016 Xavi Julian <xavier.julian@kaleidos.net>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as
 * published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program. If not, see <http://www.gnu.org/licenses/>.
 *
 * File: google-auth.coffee
 */

(function() {
  var GoogleLoginButtonDirective, module;

  GoogleLoginButtonDirective = function($window, $params, $location, $config, $events, $confirm, $auth, $navUrls, $loader) {
    var link;
    link = function($scope, $el, $attrs) {
      var auth_url, clientId, loginOnError, loginOnSuccess, loginWithGoogleAccount;
      auth_url = "https://accounts.google.com/o/oauth2/auth";
      clientId = $config.get("googleClientId", null);
      loginOnSuccess = function(response) {
        var nextUrl;
        if ($params.next && $params.next !== $navUrls.resolve("login")) {
          nextUrl = $params.next;
        } else {
          nextUrl = $navUrls.resolve("home");
        }
        $events.setupConnection();
        $location.search("next", null);
        $location.search("token", null);
        $location.search("state", null);
        $location.search("code", null);
        return $location.path(nextUrl);
      };
      loginOnError = function(response) {
        $location.search("state", null);
        $location.search("code", null);
        $loader.pageLoaded();
        if (response.data._error_message) {
          return $confirm.notify("light-error", response.data._error_message);
        } else {
          return $confirm.notify("light-error", "Error fetching credentials from Google.");
        }
      };
      loginWithGoogleAccount = function() {
        var code, data, redirectUri, token, type, url;
        type = $params.state;
        code = $params.code;
        token = $params.token;
        if (!(type === "google" && code)) {
          return;
        }
        $loader.start(true);
        url = document.createElement('a');
        url.href = $location.absUrl();
        redirectUri = url.protocol + "//" + url.hostname + (url.port === '' ? '' : ':' + url.port) + "/login";
        data = {
          code: code,
          token: token,
          redirectUri: redirectUri
        };
        return $auth.login(data, type).then(loginOnSuccess, loginOnError);
      };
      loginWithGoogleAccount();
      $el.on("click", ".button-auth", function(event) {
        var redirectToUri, url;
        url = document.createElement('a');
        url.href = $location.absUrl();
        redirectToUri = url.protocol + "//" + url.hostname + (url.port === '' ? '' : ':' + url.port) + "/login";
        url = ("" + auth_url) + "?client_id=" + clientId + "&redirect_uri=" + redirectToUri + "&state=google&scope=openid%20email&response_type=code";
        return $window.location.href = url;
      });
      return $scope.$on("$destroy", function() {
        return $el.off();
      });
    };
    return {
      link: link,
      restrict: "EA",
      template: ""
    };
  };

  module = angular.module('taigaContrib.googleAuth', []);

  module.directive("tgGoogleLoginButton", ["$window", '$routeParams', "$tgLocation", "$tgConfig", "$tgEvents", "$tgConfirm", "$tgAuth", "$tgNavUrls", "tgLoader", GoogleLoginButtonDirective]);

}).call(this);
