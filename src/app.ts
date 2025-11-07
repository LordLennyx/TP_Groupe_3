interface User {
  id: number;
  name: string;
}

const user: User = {
  id: 1,
  name: "Delbrique",
};

function greet(u: User): string {
  return `Hello ${u.name}`;
}

greet(user);
