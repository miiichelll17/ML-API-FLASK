$(document).ready(function () {
	$("#prediksi").click(function (e) {
		e.preventDefault();

		// Get File Gambar yg telah diupload pengguna
		var file_data = $('#input_gambar').prop('files')[0];
		var latitude = document.getElementById("latitude").value
		var longitude = document.getElementById("longitude").value
		var pics_data = new FormData();

		pics_data.append('image', file_data);
		pics_data.append('latitude', latitude);
		pics_data.append('longitude', longitude);

		// Panggil API dengan timeout 1 detik (1000 ms)
		setTimeout(function () {
			try {
				$.ajax({
					url: "/penyakit",
					type: "POST",
					data: pics_data,
					processData: false,
					contentType: false,
					success: function (res) {
						// Ambil hasil prediksi dan path gambar yang diprediksi dari API
						res_pesan = res['data']


						// Tampilkan hasil prediksi ke halaman web
						generate_prediksi(res_pesan);
					}
				});
			} catch (e) {
				// Jika gagal memanggil API, tampilkan error di console
				console.log("Gagal !");
				console.log(e);
			}
		}, 1000)
	})

	// Fungsi untuk menampilkan hasil prediksi model
	function generate_prediksi(res_pesan) {
		var str = "";
		str += "<h3>Hasil Prediksi </h3>";
		str += "<br>";
		str += "<h3>" + res_pesan['nama_penyakit'] + "</h3>";
		$("#hasil_prediksi").html(str);
	}
})