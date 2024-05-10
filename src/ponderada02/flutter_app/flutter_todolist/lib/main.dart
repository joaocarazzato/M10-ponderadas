import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';



void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter App',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.lightGreen),
        useMaterial3: true,
      ),
      home: const MyHomePage(title: 'Flutter To-do List'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title});

  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}


class _MyHomePageState extends State<MyHomePage> {
  final TextEditingController _controllername = TextEditingController();
  final TextEditingController _controllerdata = TextEditingController();
  final TextEditingController _controllerpostedit = TextEditingController();
  final TextEditingController _controllercontentedit = TextEditingController();
  List all_posts = [];

  void initState() {
    super.initState();
    print("INIT STATE CALLED");
    getAllPosts();
    print("got all posts.");
  }
    
    

  void requestCaller() async {
    var resposta = await http.post(Uri.parse("http://10.0.2.2:5000/posts"),
    headers: <String, String>{
      'Content-Type': 'application/json; charset=UTF-8',
      }, 
    body: jsonEncode({
      'post_name': _controllername.text, 
      'post_content': _controllerdata.text
      })
      );
      setState(() {
        getAllPosts();
        print("got all posts.");
      });

      print(resposta.body);
  }

  void postEditor(id) async {
    var resposta = await http.put(Uri.parse("http://10.0.2.2:5000/posts/${id}"),
    headers: <String, String>{
      'Content-Type': 'application/json; charset=UTF-8',
      }, 
    body: jsonEncode({
      'post_name': _controllerpostedit.text, 
      'post_content': _controllercontentedit.text
      })
      );
      setState(() {
        getAllPosts();
        print("got all posts.");
      });

      print(resposta.body);
  }
  
  void postDeleter(id) async {
    var resposta = await http.delete(Uri.parse("http://10.0.2.2:5000/posts/${id}"),
    headers: <String, String>{
      'Content-Type': 'application/json; charset=UTF-8',
      }, 
      );
      setState(() {
        getAllPosts();
        print("got all posts.");
      });

      print(resposta.body);
  }

  void getAllPosts() async {
    var resposta = await http.get(Uri.parse("http://10.0.2.2:5000/posts")
      );

      var processedanswer = jsonDecode(resposta.body);
      print(resposta.body);
      setState(() {
        all_posts = [];
        all_posts = processedanswer;
      });

      print(all_posts.length);
  }

  void showMyDialog() async {
  return showDialog<void>(
        context: context,
        builder: (BuildContext context) => AlertDialog(
          title: const Text('Adicionar Tarefa'),
          content: const Text('Adicionar tarefa a To-do List'),
          actions: <Widget>[
          TextField(
            controller: _controllername,
            decoration: const InputDecoration(
            border: OutlineInputBorder(),
            labelText: 'Nome do seu post'
              ),
            ),
            TextField(
            controller: _controllerdata,
            decoration: const InputDecoration(
            border: OutlineInputBorder(),
            labelText: 'Diga o que você está pensando...'
              ),
            ),
            Row(
              children: [
              TextButton(
                onPressed: () => Navigator.pop(context, 'Cancelar'),
                // onPressed: () => getAllPosts(),

                child: const Text('Cancelar'),
              ),
              TextButton(
                onPressed: () {
                  requestCaller();
                  Navigator.pop(context, 'Adicionar');
                  },
                child: const Text('Adicionar'),
              ),
              ],
            )
          ],
        ),
      );
}

  void showDialogPosts(postid, postname, postcontent) async {
    _controllerpostedit.text = postname;
    _controllercontentedit.text = postcontent;
  return showDialog<void>(
        context: context,
        builder: (BuildContext contexteditor) => AlertDialog(
          title: const Text('Editar Tarefa'),
          content: const Text('Editar tarefa da To-do List'),
          actions: <Widget>[
          TextField(
            controller: _controllerpostedit,
            decoration: const InputDecoration(
            border: OutlineInputBorder(),
            labelText: 'Nome do seu post'
              ),
            ),
            TextField(
            controller: _controllercontentedit,
            decoration: const InputDecoration(
            border: OutlineInputBorder(),
            labelText: 'Diga o que você está pensando...'
              ),
            ),
            Row(
              children: [
              TextButton(
                onPressed: () => Navigator.pop(contexteditor, 'Cancelar'),
                // onPressed: () => getAllPosts(),

                child: const Text('Cancelar'),
              ),
              TextButton(
                onPressed: () {
                  postEditor(postid);
                  Navigator.pop(contexteditor, 'Atualizar');
                  },
                child: const Text('OK'),
              ),
              ],
            )
          ],
        ),
      );
}

  void showDialogPostsDelete(postid) async {
  return showDialog<void>(
        context: context,
        builder: (BuildContext contextdeleter) => AlertDialog(
          title: const Text('Você tem certeza?'),
          content: const Text('Deletar tarefa da To-do List?'),
          actions: <Widget>[
            Row(
              children: [
              TextButton(
                onPressed: () => Navigator.pop(contextdeleter, 'Cancelar'),
                // onPressed: () => getAllPosts(),

                child: const Text('Cancelar'),
              ),
              TextButton(
                onPressed: () {
                  postDeleter(postid);
                  Navigator.pop(contextdeleter, 'Deletar');
                  },
                child: const Text('OK'),
              ),
              ],
            )
          ],
        ),
      );
}

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        // Here we take the value from the MyHomePage object that was created by
        // the App.build method, and use it to set our appbar title.
        title: Text(widget.title),
      ),
      body: Center(
        // Center is a layout widget. It takes a single child and positions it
        // in the middle of the parent.
        child: Column(
          verticalDirection: VerticalDirection.down,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
              const Text("Últimas tarefas",
              style: TextStyle(fontWeight: FontWeight.bold, fontSize: 26, height: 2),
              ),
              ListView.builder(
                itemCount: all_posts.length,
                scrollDirection: Axis.vertical,
                shrinkWrap: true,
                itemBuilder: (context,index){
                return ListTile(
                  // title:Text("${all_posts[index]}")
                  title: Container(
                    decoration: BoxDecoration(
                            borderRadius: BorderRadius.circular(8.0),
                            border: const Border.fromBorderSide(BorderSide(width: 2))
                    ),
                    alignment: Alignment.center,
                    width: 350,
                    height: 100,
                    child: Column(
                      children: [
                        Text("[${all_posts[index]['id']}] ${all_posts[index]['post_name']}"),
                        Text("${all_posts[index]["post_content"]}"),
                        Align(
                          alignment: Alignment.bottomRight,
                          child: Row(
                            mainAxisAlignment: MainAxisAlignment.end,
                            children: [
                            TextButton(onPressed: () {
                              showDialogPosts(all_posts[index]['id'], all_posts[index]['post_name'], all_posts[index]["post_content"]);
                              }, 
                              child: const Icon(Icons.edit, size: 20,)),
                            TextButton(onPressed: () {
                              showDialogPostsDelete(all_posts[index]['id']);
                              }, 
                              child: const Icon(Icons.delete, size: 20,)),
                          ],)
                          ),
                        
                      ],
                    ),
                  )
                );
        }
        ),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton(
                    onPressed: () {showMyDialog();},
                    child: const Icon(Icons.add),
                    ), // This trailing comma makes auto-formatting nicer for build methods.
    );
  }
}
