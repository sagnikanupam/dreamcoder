

let string_of_chars chars = 
  let buf = Buffer.create 16 in
  List.iter (Buffer.add_char buf) chars;
  Buffer.contents buf

let cc_rotate = fun s -> string_of_chars [s.[6]; s.[3]; s.[0]; s.[7]; s.[4]; s.[1]; s.[8]; s.[5]; s.[2]]

let _op_prime = fun s op -> 
  op (op (op s))
(* operation X = X' *)

let _rotate_front = fun s ->
  (* F operation on Rubik's Cube *)
  let faces =  String.split_on_char '|' s in
  let cubeU = List.nth faces 0 in 
  let cubeF = List.nth faces 1 in
  let cubeR = List.nth faces 2 in 
  let cubeB = List.nth faces 3 in
  let cubeL = List.nth faces 4 in
  let cubeD = List.nth faces 5 in
    let newF = cc_rotate cubeF in 
    let temp = String.sub cubeU 6 ((String.length cubeU)-6) in
    let newU = (String.sub cubeU 0 6)^(string_of_chars [cubeL.[8]; cubeL.[5]; cubeL.[2]]) in
    let temp2 = string_of_chars [cubeR.[0]; cubeR.[3]; cubeR.[6]] in
    let newR = string_of_chars [temp.[0]; cubeR.[1]; cubeR.[2]; temp.[1]; cubeR.[4]; cubeR.[5]; temp.[2]; cubeR.[7]; cubeR.[8]] in
    let temp3 = string_of_chars [cubeD.[2]; cubeD.[1]; cubeD.[0]] in 
    let newD = temp2^(String.sub cubeD 3 ((String.length cubeD)-3)) in
    let newL = string_of_chars [cubeL.[0]; cubeL.[1]; temp3.[0]; cubeL.[3]; cubeL.[4]; temp3.[1]; cubeL.[6]; cubeL.[7]; temp3.[2]] in
      String.concat "|" [newU; newF; newR; cubeB; newL; newD]

let _rotate_back = fun s ->
  (* B operation on Rubik's Cube *) 
  let faces =  String.split_on_char '|' s in
  let cubeU = List.nth faces 0 in 
  let cubeF = List.nth faces 1 in
  let cubeR = List.nth faces 2 in 
  let cubeB = List.nth faces 3 in
  let cubeL = List.nth faces 4 in
  let cubeD = List.nth faces 5 in
    let newB = cc_rotate cubeB in 
    let temp = string_of_chars [cubeU.[2]; cubeU.[1]; cubeU.[0]] in
    let newU = (string_of_chars [cubeR.[2]; cubeR.[5]; cubeR.[8]])^(String.sub cubeU 3 ((String.length cubeU)-3)) in
    let temp2 = string_of_chars [cubeL.[6]; cubeL.[3]; cubeL.[0]] in
    let newL = string_of_chars [temp.[0]; cubeL.[1]; cubeL.[2]; temp.[1]; cubeL.[4]; cubeL.[5]; temp.[2]; cubeL.[7]; cubeL.[8]] in
    let temp3 = string_of_chars [cubeD.[6]; cubeD.[7]; cubeD.[8]] in 
    let newD = (String.sub cubeD 0 6)^temp2 in
    let newR = string_of_chars [cubeR.[0]; cubeR.[1]; temp3.[0]; cubeR.[3]; cubeR.[4]; temp3.[1]; cubeR.[6]; cubeR.[7]; temp3.[2]] in
      String.concat "|" [newU; cubeF; newR; newB; newL; newD]

let _rotate_left = fun s -> 
  (* L operation on Rubik's Cube *)
  let faces =  String.split_on_char '|' s in
  let cubeU = List.nth faces 0 in 
  let cubeF = List.nth faces 1 in
  let cubeR = List.nth faces 2 in 
  let cubeB = List.nth faces 3 in
  let cubeL = List.nth faces 4 in
  let cubeD = List.nth faces 5 in
    let newL = cc_rotate cubeL in 
    let temp = string_of_chars [cubeU.[0]; cubeU.[3]; cubeU.[6]] in
    let newU = string_of_chars [cubeB.[8]; cubeU.[1]; cubeU.[2]; cubeB.[5]; cubeU.[4]; cubeU.[5]; cubeB.[2]; cubeU.[7]; cubeU.[8]] in
    let temp2 = string_of_chars [cubeF.[0]; cubeF.[3]; cubeF.[6]] in
    let newF = string_of_chars [temp.[0]; cubeF.[1]; cubeF.[2]; temp.[1]; cubeF.[4]; cubeF.[5]; temp.[2]; cubeF.[7]; cubeF.[8]] in
    let temp3 = string_of_chars [cubeD.[8]; cubeD.[5]; cubeD.[2]] in 
    let newD = string_of_chars [cubeD.[0]; cubeD.[1]; temp2.[0]; cubeD.[3]; cubeD.[4]; temp2.[1]; cubeD.[6]; cubeD.[7]; temp2.[2]] in
    let newB = string_of_chars [cubeB.[0]; cubeB.[1]; temp3.[0]; cubeB.[3]; cubeB.[4]; temp3.[1]; cubeB.[6]; cubeB.[7]; temp3.[2]] in
      String.concat "|" [newU; newF; cubeR; newB; newL; newD]

let _rotate_right = fun s -> 
  (* R operation on Rubik's Cube *)
  let faces =  String.split_on_char '|' s in
  let cubeU = List.nth faces 0 in 
  let cubeF = List.nth faces 1 in
  let cubeR = List.nth faces 2 in 
  let cubeB = List.nth faces 3 in
  let cubeL = List.nth faces 4 in
  let cubeD = List.nth faces 5 in
    let newR = cc_rotate cubeR in 
    let temp = string_of_chars [cubeU.[8]; cubeU.[5]; cubeU.[2]] in
    let newU = string_of_chars [cubeU.[0]; cubeU.[1]; cubeF.[2]; cubeU.[3]; cubeU.[4]; cubeF.[5]; cubeU.[6]; cubeU.[7]; cubeF.[8]] in
    let temp2 = string_of_chars [cubeB.[6]; cubeB.[3]; cubeB.[0]] in
    let newB = string_of_chars [temp.[0]; cubeB.[1]; cubeB.[2]; temp.[1]; cubeB.[4]; cubeB.[5]; temp.[2]; cubeB.[7]; cubeB.[8]] in
    let temp3 = string_of_chars [cubeD.[0]; cubeD.[3]; cubeD.[6]] in 
    let newD = string_of_chars [temp2.[0]; cubeD.[1]; cubeD.[2]; temp2.[1]; cubeD.[4]; cubeD.[5]; temp2.[2]; cubeD.[7]; cubeD.[8]] in
    let newF = string_of_chars [cubeF.[0]; cubeF.[1]; temp3.[0]; cubeF.[3]; cubeF.[4]; temp3.[1]; cubeF.[6]; cubeF.[7]; temp3.[2]] in
      String.concat "|" [newU; newF; newR; newB; cubeL; newD]      

let _rotate_up = fun s -> 
  (* U operation on Rubik's Cube *)
  let faces =  String.split_on_char '|' s in
  let cubeU = List.nth faces 0 in 
  let cubeF = List.nth faces 1 in
  let cubeR = List.nth faces 2 in 
  let cubeB = List.nth faces 3 in
  let cubeL = List.nth faces 4 in
  let cubeD = List.nth faces 5 in
    let newU = cc_rotate cubeU in 
    let temp = String.sub cubeF 0 3 in
    let newF = (String.sub cubeR 0 3)^(String.sub cubeF 3 ((String.length cubeF)-3)) in
    let temp2 = String.sub cubeL 0 3 in
    let newL = temp^(String.sub cubeL 3 ((String.length cubeL)-3)) in
    let temp3 = String.sub cubeB 0 3 in 
    let newB = temp2^(String.sub cubeB 3 ((String.length cubeB)-3)) in
    let newR = temp3^(String.sub cubeR 3 ((String.length cubeR)-3)) in
      String.concat "|" [newU; newF; newR; newB; newL; cubeD]      

let _rotate_down = fun s -> 
  (* D operation on Rubik's Cube *)
  let faces =  String.split_on_char '|' s in
  let cubeU = List.nth faces 0 in 
  let cubeF = List.nth faces 1 in
  let cubeR = List.nth faces 2 in 
  let cubeB = List.nth faces 3 in
  let cubeL = List.nth faces 4 in
  let cubeD = List.nth faces 5 in
    let newD = cc_rotate cubeD in 
    let temp = String.sub cubeF 6 ((String.length cubeF)-6) in
    let newF = (String.sub cubeF 0 6)^(String.sub cubeL 6 ((String.length cubeF)-6)) in
    let temp2 = String.sub cubeR 6 ((String.length cubeR)-6) in
    let newR = (String.sub cubeR 0 6)^temp in
    let temp3 = String.sub cubeB 6 ((String.length cubeB)-6) in 
    let newB = (String.sub cubeB 0 6)^temp2 in
    let newL = (String.sub cubeL 0 6)^temp3 in
      String.concat "|" [cubeU; newF; newR; newB; newL; newD]

let _rotate_up_prime = fun s -> _op_prime s _rotate_up
(* U' operation on Rubik's Cube *)

let _rotate_down_prime = fun s -> _op_prime s _rotate_down
(* D' operation on Rubik's Cube *)

let _rotate_front_prime = fun s -> _op_prime s _rotate_front
(* F' operation on Rubik's Cube *)

let _rotate_back_prime = fun s -> _op_prime s _rotate_back
(* B' operation on Rubik's Cube *)

let _rotate_left_prime = fun s -> _op_prime s _rotate_left
(* L' operation on Rubik's Cube *)

let _rotate_right_prime = fun s -> _op_prime s _rotate_right
(* R' operation on Rubik's Cube *)
  
(*

(* Test *)
let solved_conf = "rrrrrrrrr|bbbbbbbbb|wwwwwwwww|ggggggggg|yyyyyyyyy|ooooooooo" in 
_rotate_down solved_conf |> print_string
*)