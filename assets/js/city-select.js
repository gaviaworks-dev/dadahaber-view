  const prayerCities = [
    { name: "Adana",      times: ["06:31","12:48","16:18","19:02","20:22"] },
    { name: "Adıyaman",   times: ["06:24","12:41","16:11","18:55","20:17"] },
    { name: "Afyon",      times: ["06:46","13:06","16:36","19:20","20:42"] },
    { name: "Ağrı",       times: ["06:08","12:24","15:54","18:37","20:00"] },
    { name: "Aksaray",    times: ["06:36","12:54","16:24","19:08","20:30"] },
    { name: "Amasya",     times: ["06:34","12:51","16:22","19:06","20:28"] },
    { name: "Ankara",     times: ["06:41","13:05","16:35","19:18","20:40"] },
    { name: "Antalya",    times: ["06:44","13:02","16:30","19:15","20:37"] },
    { name: "Ardahan",    times: ["06:12","12:28","15:58","18:42","20:05"] },
    { name: "Artvin",     times: ["06:18","12:34","16:04","18:48","20:11"] },
    { name: "Aydın",      times: ["06:56","13:18","16:49","19:34","20:57"] },
    { name: "Balıkesir",  times: ["06:52","13:14","16:45","19:28","20:51"] },
    { name: "Bartın",     times: ["06:43","13:03","16:34","19:17","20:40"] },
    { name: "Batman",     times: ["06:16","12:33","16:03","18:46","20:08"] },
    { name: "Bayburt",    times: ["06:22","12:38","16:08","18:51","20:14"] },
    { name: "Bilecik",    times: ["06:49","13:10","16:41","19:25","20:47"] },
    { name: "Bingöl",     times: ["06:19","12:35","16:05","18:49","20:11"] },
    { name: "Bitlis",     times: ["06:14","12:30","16:00","18:44","20:06"] },
    { name: "Bolu",       times: ["06:45","13:06","16:37","19:21","20:43"] },
    { name: "Burdur",     times: ["06:46","13:05","16:34","19:18","20:40"] },
    { name: "Bursa",      times: ["06:50","13:10","16:41","19:24","20:47"] },
    { name: "Çanakkale",  times: ["06:55","13:17","16:48","19:33","20:56"] },
    { name: "Çankırı",    times: ["06:39","12:57","16:28","19:12","20:34"] },
    { name: "Çorum",      times: ["06:36","12:53","16:24","19:08","20:30"] },
    { name: "Denizli",    times: ["06:48","13:07","16:36","19:20","20:43"] },
    { name: "Diyarbakır", times: ["06:18","12:35","16:05","18:48","20:10"] },
    { name: "Düzce",      times: ["06:44","13:04","16:35","19:19","20:41"] },
    { name: "Edirne",     times: ["06:58","13:19","16:51","19:36","20:59"] },
    { name: "Elazığ",     times: ["06:22","12:38","16:08","18:52","20:14"] },
    { name: "Erzincan",   times: ["06:24","12:40","16:10","18:54","20:16"] },
    { name: "Erzurum",    times: ["06:18","12:34","16:04","18:47","20:10"] },
    { name: "Eskişehir",  times: ["06:47","13:08","16:39","19:22","20:45"] },
    { name: "Gaziantep",  times: ["06:26","12:43","16:13","18:56","20:18"] },
    { name: "Giresun",    times: ["06:27","12:44","16:15","18:59","20:22"] },
    { name: "Gümüşhane", times: ["06:23","12:39","16:09","18:53","20:15"] },
    { name: "Hakkari",    times: ["06:07","12:23","15:53","18:37","19:59"] },
    { name: "Hatay",      times: ["06:24","12:41","16:11","18:54","20:16"] },
    { name: "Iğdır",      times: ["06:06","12:22","15:52","18:35","19:57"] },
    { name: "Isparta",    times: ["06:45","13:04","16:33","19:17","20:39"] },
    { name: "İstanbul",   times: ["06:48","13:14","16:45","19:31","20:52"] },
    { name: "İzmir",      times: ["06:55","13:16","16:47","19:32","20:55"] },
    { name: "Kahramanmaraş", times: ["06:25","12:42","16:12","18:55","20:17"] },
    { name: "Karabük",    times: ["06:42","13:02","16:33","19:16","20:39"] },
    { name: "Karaman",    times: ["06:38","12:58","16:27","19:11","20:33"] },
    { name: "Kars",       times: ["06:10","12:26","15:56","18:39","20:02"] },
    { name: "Kastamonu",  times: ["06:39","12:58","16:29","19:13","20:35"] },
    { name: "Kayseri",    times: ["06:33","12:51","16:21","19:05","20:27"] },
    { name: "Kırıkkale",  times: ["06:40","12:58","16:29","19:12","20:34"] },
    { name: "Kırklareli", times: ["06:55","13:17","16:49","19:34","20:57"] },
    { name: "Kırşehir",   times: ["06:37","12:55","16:25","19:09","20:31"] },
    { name: "Kilis",      times: ["06:26","12:43","16:13","18:56","20:18"] },
    { name: "Kocaeli",    times: ["06:46","13:11","16:42","19:26","20:48"] },
    { name: "Konya",      times: ["06:40","13:00","16:30","19:14","20:36"] },
    { name: "Kütahya",    times: ["06:49","13:10","16:41","19:24","20:47"] },
    { name: "Malatya",    times: ["06:22","12:39","16:09","18:53","20:15"] },
    { name: "Manisa",     times: ["06:54","13:15","16:46","19:31","20:54"] },
    { name: "Mardin",     times: ["06:17","12:34","16:04","18:47","20:09"] },
    { name: "Mersin",     times: ["06:30","12:47","16:17","19:01","20:21"] },
    { name: "Muğla",      times: ["06:52","13:12","16:42","19:27","20:50"] },
    { name: "Muş",        times: ["06:15","12:31","16:01","18:44","20:07"] },
    { name: "Nevşehir",   times: ["06:35","12:53","16:23","19:07","20:29"] },
    { name: "Niğde",      times: ["06:34","12:52","16:22","19:06","20:28"] },
    { name: "Ordu",       times: ["06:28","12:45","16:16","19:00","20:22"] },
    { name: "Osmaniye",   times: ["06:28","12:45","16:15","18:58","20:20"] },
    { name: "Rize",       times: ["06:21","12:37","16:07","18:51","20:14"] },
    { name: "Sakarya",    times: ["06:45","13:10","16:41","19:25","20:47"] },
    { name: "Samsun",     times: ["06:34","12:51","16:22","19:06","20:29"] },
    { name: "Siirt",      times: ["06:13","12:30","16:00","18:43","20:05"] },
    { name: "Sinop",      times: ["06:36","12:53","16:24","19:08","20:31"] },
    { name: "Sivas",      times: ["06:29","12:46","16:16","19:00","20:22"] },
    { name: "Şanlıurfa",  times: ["06:22","12:39","16:09","18:52","20:14"] },
    { name: "Şırnak",     times: ["06:11","12:28","15:58","18:41","20:03"] },
    { name: "Tekirdağ",   times: ["06:54","13:16","16:47","19:32","20:55"] },
    { name: "Tokat",      times: ["06:31","12:48","16:19","19:02","20:25"] },
    { name: "Trabzon",    times: ["06:23","12:39","16:10","18:54","20:17"] },
    { name: "Tunceli",    times: ["06:21","12:37","16:07","18:51","20:13"] },
    { name: "Uşak",       times: ["06:50","13:11","16:41","19:25","20:48"] },
    { name: "Van",        times: ["06:08","12:24","15:54","18:37","20:00"] },
    { name: "Yalova",     times: ["06:49","13:11","16:42","19:26","20:48"] },
    { name: "Yozgat",     times: ["06:34","12:52","16:22","19:06","20:28"] },
    { name: "Zonguldak",  times: ["06:44","13:04","16:35","19:18","20:41"] },
  ];

  let prayerSelectedCity = "İstanbul";

  function renderPrayerCityList(list) {
    const container = document.getElementById("cityListContainer");
    if (!list.length) {
      container.innerHTML = '<div id="cityNoResults">Şehir bulunamadı</div>';
      return;
    }
    container.innerHTML = list.map(c => `
      <div class="city-list-item${c.name === prayerSelectedCity ? " active" : ""}" onclick="selectPrayerCity('${c.name}')">
        ${c.name}
        ${c.name === prayerSelectedCity ? '<i class="fas fa-check" style="font-size:11px;"></i>' : ""}
      </div>
    `).join("");
  }

  function filterPrayerCities() {
    const normalize = s => s.toLowerCase()
      .replace(/ı/g,"i").replace(/İ/g,"i")
      .replace(/ğ/g,"g").replace(/ş/g,"s")
      .replace(/ç/g,"c").replace(/ö/g,"o").replace(/ü/g,"u");
    const q = normalize(document.getElementById("citySearchInput").value);
    renderPrayerCityList(prayerCities.filter(c => normalize(c.name).includes(q)));
  }

  function selectPrayerCity(name) {
    const city = prayerCities.find(c => c.name === name);
    if (!city) return;
    prayerSelectedCity = name;
    document.getElementById("prayer-city-name").textContent = name;
    document.getElementById("pt-gunes").textContent  = city.times[0];
    document.getElementById("pt-ogle").textContent   = city.times[1];
    document.getElementById("pt-ikindi").textContent = city.times[2];
    document.getElementById("pt-aksam").textContent  = city.times[3];
    document.getElementById("pt-yatsi").textContent  = city.times[4];
    bootstrap.Modal.getInstance(document.getElementById("citySelectModal")).hide();
  }

  // Modal açılınca listeyi sıfırla
  document.getElementById("citySelectModal").addEventListener("show.bs.modal", function () {
    document.getElementById("citySearchInput").value = "";
    renderPrayerCityList(prayerCities);
    // Seçili şehre scroll
    setTimeout(() => {
      const active = document.querySelector(".city-list-item.active");
      if (active) active.scrollIntoView({ block: "center" });
    }, 50);
  });