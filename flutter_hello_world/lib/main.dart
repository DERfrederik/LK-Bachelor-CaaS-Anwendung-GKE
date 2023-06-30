import 'package:english_words/english_words.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import 'dart:async';
import 'dart:convert';
import 'package:http/http.dart' as http;

Future<Weather> fetchWeather({int? timestamp}) async {
  final http.Response response;
  if (timestamp == null) {
    response =
        await http.get(Uri.parse('https://caas.lk-bachelor.de/api/weather/'));
  } else {
    response = await http.get(
      Uri.parse('https://caas.lk-bachelor.de/api/weather/')
          .replace(queryParameters: {'timestamp': '$timestamp'}),
    );
  }

  if (response.statusCode == 200) {
    // If the server did return a 200 OK response,
    // then parse the JSON.
    return Weather.fromJson(jsonDecode(response.body));
  } else {
    // If the server did not return a 200 OK response,
    // then throw an exception.
    throw Exception('Failed to load album');
  }
}

class Weather {
  final int timestamp;
  final double temp;
  final double pressure;
  final double wind;

  const Weather({
    required this.timestamp,
    required this.temp,
    required this.pressure,
    required this.wind,
  });

  factory Weather.fromJson(Map<String, dynamic> json) {
    return Weather(
      timestamp: json['timestamp'],
      temp: json['temp'],
      pressure: json['pressure'],
      wind: json['wind'],
    );
  }
}

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      create: (context) => MyAppState(),
      child: MaterialApp(
        title: 'CaaS - WetterGetter',
        theme: ThemeData(
          // useMaterial3: true,
          // colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepOrange),
          primaryColor: Colors.deepOrange,
        ),
        home: MyHomePage(),
      ),
    );
  }
}

class MyAppState extends ChangeNotifier {
  var current = WordPair.random();
  var historic = WordPair.random();
  Weather currentWeather = Weather(timestamp: 0, temp: 0, pressure: 0, wind: 0);
  Weather historicWeather =
      Weather(timestamp: 0, temp: 0, pressure: 0, wind: 0);

  void getNextAktuellesWetter() async {
    current = WordPair.random();
    currentWeather = await fetchWeather();
    notifyListeners();
  }

  void getNextHistorischesWetter({int? userInput}) async {
    historic = WordPair.random();
    historicWeather = await fetchWeather(timestamp: userInput);
    notifyListeners();
  }
}

class MyHomePage extends StatelessWidget {
  final _textController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    var appState = context.watch<MyAppState>();

    return Scaffold(
      appBar: AppBar(title: Center(child: const Text('Wetter Getter'))),
      body: Column(
        mainAxisSize: MainAxisSize.max,
        children: [
          SizedBox(
            height: 30,
          ),
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text(
                'Aktuelle Wetterdaten:',
                style: TextStyle(fontSize: 25),
              ),
            ],
          ),
          SizedBox(
            height: 30,
          ),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: [
              Column(
                children: [
                  Text(
                    'Datum und Zeit',
                    style: TextStyle(fontWeight: FontWeight.bold),
                  ),
                  Text(appState.currentWeather.timestamp.toString()),
                ],
              ),
              Column(
                children: [
                  Text(
                    'Temperatur',
                    style: TextStyle(fontWeight: FontWeight.bold),
                  ),
                  Text(appState.currentWeather.temp.toString()),
                ],
              ),
              Column(
                children: [
                  Text(
                    'Luftdruck',
                    style: TextStyle(fontWeight: FontWeight.bold),
                  ),
                  Text(appState.currentWeather.pressure.toString()),
                ],
              ),
              Column(
                children: [
                  Text(
                    'Windgeschwindigkeit',
                    style: TextStyle(fontWeight: FontWeight.bold),
                  ),
                  Text(appState.currentWeather.wind.toString()),
                ],
              ),
            ],
          ),
          SizedBox(
            height: 30,
          ),
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Column(
                children: [
                  ElevatedButton(
                    onPressed: () {
                      appState.getNextAktuellesWetter();
                    },
                    child: Text('Aktuelle Wetterdaten aktualisieren'),
                  ),
                ],
              ),
            ],
          ),
          const Divider(
            height: 100,
            thickness: 1,
            indent: 20,
            endIndent: 20,
            color: Colors.black,
          ),
          SizedBox(
            height: 10,
          ),
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text(
                'Historische Wetterdaten:',
                style: TextStyle(fontSize: 25),
              ),
            ],
          ),
          SizedBox(
            height: 30,
          ),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: [
              Column(
                children: [
                  Text(
                    'Datum und Zeit',
                    style: TextStyle(fontWeight: FontWeight.bold),
                  ),
                  Text(appState.historicWeather.timestamp.toString()),
                ],
              ),
              Column(
                children: [
                  Text(
                    'Temperatur',
                    style: TextStyle(fontWeight: FontWeight.bold),
                  ),
                  Text(appState.historicWeather.temp.toString()),
                ],
              ),
              Column(
                children: [
                  Text(
                    'Luftdruck',
                    style: TextStyle(fontWeight: FontWeight.bold),
                  ),
                  Text(appState.historicWeather.pressure.toString()),
                ],
              ),
              Column(
                children: [
                  Text(
                    'Windgeschwindigkeit',
                    style: TextStyle(fontWeight: FontWeight.bold),
                  ),
                  Text(appState.historicWeather.wind.toString()),
                ],
              ),
            ],
          ),
          SizedBox(
            height: 25,
          ),
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text(
                'Historische Daten zu folgendem Timestamp:',
                style: TextStyle(fontSize: 15),
              ),
            ],
          ),
          SizedBox(
            height: 10,
          ),
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              SizedBox(
                width: 300,
                child: TextField(
                  controller: _textController,
                  decoration: InputDecoration(
                    hintText: '1679923852',
                    border: const OutlineInputBorder(),
                  ),
                ),
              ),
            ],
          ),
          SizedBox(
            height: 30,
          ),
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Column(
                children: [
                  ElevatedButton(
                    onPressed: () {
                      appState.getNextHistorischesWetter(
                        userInput: int.parse(_textController.text),
                      );
                    },
                    child: Text('Historische Wetterdaten laden'),
                  ),
                ],
              ),
            ],
          ),
        ],
      ),
    );
  }
}
