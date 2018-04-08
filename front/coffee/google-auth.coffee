###
# Copyright (C) 2018 Don Bowman <db@donbowman.ca>
# Copyright (C) 2014-2016 Andrey Antukh <niwi@niwi.nz>
# Copyright (C) 2014-2016 Jesús Espino Garcia <jespinog@gmail.com>
# Copyright (C) 2014-2016 David Barragán Merino <bameda@dbarragan.com>
# Copyright (C) 2014-2016 Alejandro Alonso <alejandro.alonso@kaleidos.net>
# Copyright (C) 2014-2016 Juan Francisco Alcántara <juanfran.alcantara@kaleidos.net>
# Copyright (C) 2014-2016 Xavi Julian <xavier.julian@kaleidos.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# File: google-auth.coffee
###

GoogleLoginButtonDirective = ($window, $params, $location, $config, $events, $confirm,
                              $auth, $navUrls, $loader) ->
    # Login or registar a user with his/her google account.
    #
    # Example:
    #     tg-google-login-button()
    #
    # Requirements:
    #   - ...

    link = ($scope, $el, $attrs) ->
        auth_url = "https://accounts.google.com/o/oauth2/auth"
        clientId = $config.get("googleClientId", null)

        loginOnSuccess = (response) ->
            if $params.next and $params.next != $navUrls.resolve("login")
                nextUrl = $params.next
            else
                nextUrl = $navUrls.resolve("home")

            $events.setupConnection()

            $location.search("next", null)
            $location.search("token", null)
            $location.search("state", null)
            $location.search("code", null)
            $location.path(nextUrl)

        loginOnError = (response) ->
            $location.search("state", null)
            $location.search("code", null)
            $loader.pageLoaded()

            if response.data._error_message
                $confirm.notify("light-error", response.data._error_message )
            else
                $confirm.notify("light-error", "Error obtaining credentials from Google.")

        loginWithGoogleAccount = ->
            type = $params.state
            code = $params.code
            token = $params.token

            return if not (type == "google" and code)
            $loader.start(true)

            url = document.createElement('a')
            url.href = $location.absUrl()
            redirectUri = "#{url.protocol}//#{url.hostname}#{if url.port == '' then '' else ':'+url.port}/login"

            data = {code: code, token: token, redirectUri: redirectUri}
            $auth.login(data, type).then(loginOnSuccess, loginOnError)

        loginWithGoogleAccount()

        $el.on "click", ".button-auth", (event) ->
            url = document.createElement('a')
            url.href = $location.absUrl()
            redirectToUri = "#{url.protocol}//#{url.hostname}#{if url.port == '' then '' else ':'+url.port}/login"

            url = "#{auth_url}" + "?client_id=" + clientId + "&redirect_uri=" + redirectToUri + "&state=google&scope=openid%20email&response_type=code";

            $window.location.href = url

        $scope.$on "$destroy", ->
            $el.off()

    return {
        link: link
        restrict: "EA"
        template: ""
    }

module = angular.module('taigaContrib.googleAuth', [])
module.directive("tgGoogleLoginButton", ["$window", '$routeParams', "$tgLocation", "$tgConfig", "$tgEvents",
                                         "$tgConfirm", "$tgAuth", "$tgNavUrls", "tgLoader",
                                         GoogleLoginButtonDirective])
