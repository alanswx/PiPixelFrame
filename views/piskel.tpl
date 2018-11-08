      window.pskl.appEnginePiskelData_ = {
        piskel : {{!piskel}},
        isLoggedIn : true,
        fps : {{anim['fps']}},
        descriptor : {
          name : "{{anim['name']}}",
          description : "{{anim['description']}}",
          isPublic : {{anim.get('public', "false")}}
        }
      };
