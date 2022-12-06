import { getServicesOptions } from "$lib/services";

import type { PageLoad } from "./$types";

export const load: PageLoad = async ({ url, parent }) => {
  await parent();

  const query = url.searchParams;
  const source = query.get("utm_source");

  return {
    servicesOptions: await getServicesOptions(),
    source,
  };
};
