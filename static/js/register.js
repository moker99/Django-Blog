$(function(){
    function bindCaptchaBtnClick(){
        $('#captcha-btn').click(function(event){
            let $this = $(this);
            let email = $('input[name="email"]').val();
            if(!email){
                alert('請先輸入 email !!')
                return;
            }
            console.log(email);
            //取消按鈕點擊事件
            $this.off('click ');
            // 發送ajax請求
            $.ajax('/auth/captcha?email=' + email, {
                method: 'GET',
                success: function(result) {
                    if(result['code'] == 200) {
                        alert('驗證瑪發送成功!');
                    }else {
                        alert(result['message']);
                    }
                },
                fail: function(error) {
                    console.log(error);
                }
            })

            // 倒數計時
            let countdown = 6;
            let timer = setInterval(function(){
                if(countdown <= 0){
                    $this.text('獲取驗證碼')
                    // 清掉定時器
                    clearInterval(timer);
                    // 重新綁定點擊事件
                    bindCaptchaBtnClick();
                }else{
                    countdown--;
                    $this.text(countdown + 's')
                }
            },1000);
        })
    }

    bindCaptchaBtnClick();
});