$(document).ready(function(){
  
  // -[Animasi Scroll]---------------------------
  
  $(".navbar a, footer a[href='#halamanku']").on('click', function(event) {
    if (this.hash !== "") {
      event.preventDefault();
      var hash = this.hash;
      $('html, body').animate({
        scrollTop: $(hash).offset().top
      }, 900, function(){
        window.location.hash = hash;
      });
    } 
  });
  
  $(window).scroll(function() {
    $(".slideanim").each(function(){
      var pos = $(this).offset().top;
      var winTop = $(window).scrollTop();
        if (pos < winTop + 600) {
          $(this).addClass("slide");
        }
    });
  });
  
  // -[Prediksi Model]---------------------------
  
  // Fungsi untuk memanggil API ketika tombol prediksi ditekan
  $("#register").click(function(e) {
    e.preventDefault();
	
	// Get File Gambar yg telah diupload pengguna
    var username = $('#username').prop('text');
	  var password = $('#password').prop('text');
    var pics_data = new FormData();
    pics_data.append('username', username);
	  pics_data.append('password', password);

	// Panggil API dengan timeout 1 detik (1000 ms)
    setTimeout(function() {
	  try {
			$.ajax({
				url         : "/register",
				type        : "POST",
				data        : pics_data,
				processData : false,
				contentType : false,
				success     : function(res){
					// Ambil hasil prediksi dan path gambar yang diprediksi dari API
					res_pesan  = res['pesan']
				
					
					// Tampilkan hasil prediksi ke halaman web
					generate_prediksi(res_pesan); 
			  }
			});
		}
		catch(e) {
			// Jika gagal memanggil API, tampilkan error di console
			console.log("Gagal !");
			console.log(e);
		} 
    }, 1000)  
  })
   
  // Fungsi untuk menampilkan hasil prediksi model
  function generate_prediksi(data_prediksi, image_prediksi) {
	var str="";
		str += "<h3>Hasil Prediksi </h3>";
		str += "<br>";
		str += "<h3>" + res_pesan + "</h3>";
	$("#hasil_prediksi").html(str);
  }  
})
  
