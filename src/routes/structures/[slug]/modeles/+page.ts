import { browser } from "$app/environment";
import { userInfo } from "$lib/auth";
import { error } from "@sveltejs/kit";
import { get } from "svelte/store";
import { structure } from "../_store";

export async function load({ parent }) {
  await parent();

  // sur le serveur, info est toujours null,
  // on retourne une 404 uniquement sur le client
  if (!browser) {
    return {};
  }

  const info = get(userInfo);
  const struct = get(structure);

  const isMember = struct.isMember || info?.isBizdev || info?.isStaff;

  if (!info || !struct || !isMember) {
    throw error(404, "Page Not Found");
  }

  return {};
}
