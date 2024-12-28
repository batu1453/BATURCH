if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $username = $_POST['username'];

    // Telegram API ile doğrulama işlemi yapın (yukarıdaki gibi)
    // Eğer kullanıcı adı doğruysa, yönlendirme yapılacak
    if (username_doğru()) {
        header("Location: https://a.com");
    } else {
        echo "Geçersiz kullanıcı adı!";
    }
}
