function getLongLiveToken(data){

        FB.api('oauth/access_token', {
            client_id: data.client_id, // FB_APP_ID
            client_secret: data.secret, // FB_APP_SECRET
            grant_type: 'fb_exchange_token',
            fb_exchange_token: data.access_token // USER_TOKEN
        }, function (res) {
            if(!res || res.error) {
                console.log(!res ? 'error occurred' : res.error);
            }else{
                var accessToken = res.access_token;
                if(typeof accessToken != 'undefined'){
                }
            }
        });