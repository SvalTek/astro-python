import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';
import { APP_NAME, APP_DESCRIPTION } from '../consts';

export async function GET(context) {
  const docs = await getCollection('docs');
  return rss({
    title: APP_NAME,
    description: APP_DESCRIPTION,
    site: context.site,
    items: docs.map((document) => ({
      ...document.data,
      link: `/docs/${document.slug}/`,
    })),
  });
}
