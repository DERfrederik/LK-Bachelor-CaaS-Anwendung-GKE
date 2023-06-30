import 'package:http/http.dart' as http;

const String baseUrl = 'http://127.0.0.1:8000';

class BaseClient {
  var client = http.Client();
  Future<dynamic> getWeather(String api, {int? timestamp}) async {
    final params = timestamp != null ? {'timestamp': '$timestamp'} : null;
    var url = Uri.parse(baseUrl + api).replace(queryParameters: params);
    var response = await client.get(
      url,
      headers: {
        'Content-Type': 'application/json',
      },
    );
    if (response.statusCode == 200) {
      return response.body;
    } else {
      // Fehler UI werfen
    }
  }
}


// dart
// Copy code
// import 'dart:convert';

// Future<void> fetchPosts({int? userId}) async {
//   final url = Uri.parse('https://jsonplaceholder.typicode.com/posts');
//   final params = userId != null ? {'userId': '$userId'} : null;
//   final response = await http.get(url, headers: {
//     'Content-Type': 'application/json',
//   }, params: params,);
//   if (response.statusCode == 200) {
//     final data = jsonDecode(response.body);
//     print(data);
//   } else {
//     print('Request failed with status: ${response.statusCode}.');
//   }
// }