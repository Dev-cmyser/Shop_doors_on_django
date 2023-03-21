// let center = [55.75399399999374, 37.62209300000001];

// function init() {
//     let map = new ymaps.Map('YMapsID', {
//         center: center,
//         zoom: 8
//     });
//     // Создаем геообъект с типом геометрии "Точка".
//     myGeoObject = new ymaps.GeoObject({
//         // Описание геометрии.
//         geometry: {
//             type: "Point",
//             coordinates: [55.8, 37.8]
//         },
//         // Свойства.
//         properties: {
//             // Контент метки.
//             iconContent: 'Я тащусь',
//             hintContent: 'Ну давай уже тащи'
//         }
//     }, {
//         // Опции.
//         // Иконка метки будет растягиваться под размер ее содержимого.
//         preset: 'islands#blackStretchyIcon',
//         // Метку можно перемещать.
//         draggable: true
//     }),

//     // 	map.controls.remove('geolocationControl'); // удаляем геолокацию
//     //   map.controls.remove('searchControl'); // удаляем поиск
//     //   map.controls.remove('trafficControl'); // удаляем контроль трафика
//     //   map.controls.remove('typeSelector'); // удаляем тип
//     //   map.controls.remove('fullscreenControl'); // удаляем кнопку перехода в полноэкранный режим
//     //   map.controls.remove('zoomControl'); // удаляем контрол зуммирования
//     //   map.controls.remove('rulerControl'); // удаляем контрол правил
//     //   map.behaviors.disable(['scrollZoom']); // отключаем скролл карты (опционально)
// }



    
function init() {
    var myMap = new ymaps.Map("YMapsID", {
            center: [55.76, 37.64],
            zoom: 11
        }, {
            searchControlProvider: 'yandex#search'
        });

    // Создаем геообъект с типом геометрии "Точка".
        
        

    myMap.geoObjects
        
        .add(new ymaps.Placemark([55.674843, 37.435023], {
            balloonContent: 'двери у нас!',
            iconCaption: 'Магазин 3'
        }, {
            preset: 'islands#greenDotIconWithCaption'
        }))
        .add(new ymaps.Placemark([55.8, 37.8], {
            balloonContent: 'двери у нас!',
            iconCaption: 'Магазин 1'
        }, {
            preset: 'islands#greenDotIconWithCaption'
        }))
        .add(new ymaps.Placemark([55.694843, 37.435023], {
            balloonContent: 'двери у нас!',
            iconCaption: 'Магазин 2'
        }, {
            preset: 'islands#greenDotIconWithCaption'
        }));
        
}


ymaps.ready(init);  