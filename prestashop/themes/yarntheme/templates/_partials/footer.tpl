{**
 * Copyright since 2007 PrestaShop SA and Contributors
 * PrestaShop is an International Registered Trademark & Property of PrestaShop SA
 *
 * NOTICE OF LICENSE
 *
 * This source file is subject to the Academic Free License 3.0 (AFL-3.0)
 * that is bundled with this package in the file LICENSE.md.
 * It is also available through the world-wide-web at this URL:
 * https://opensource.org/licenses/AFL-3.0
 * If you did not receive a copy of the license and are unable to
 * obtain it through the world-wide-web, please send an email
 * to license@prestashop.com so we can send you a copy immediately.
 *
 * DISCLAIMER
 *
 * Do not edit or add to this file if you wish to upgrade PrestaShop to newer
 * versions in the future. If you wish to customize PrestaShop for your
 * needs please refer to https://devdocs.prestashop.com/ for more information.
 *
 * @author    PrestaShop SA and Contributors <contact@prestashop.com>
 * @copyright Since 2007 PrestaShop SA and Contributors
 * @license   https://opensource.org/licenses/AFL-3.0 Academic Free License 3.0 (AFL-3.0)
 *}

<div id="footer-assurance">
<div class="container">
    <div class="row">
	{hook h='displayReassurance' mod='yarn_assurance'}
    </div>
</div>
</div>

<div class="container" id="footer-main">
  <div class="row">
    {block name='hook_footer_before'}
      {hook h='displayFooterBefore'}
    {/block}
  </div>
<div class="footer-container">
  <div class="container">
    <div class="row">
      {block name='hook_footer'}
        {hook h='displayFooter'}
      {/block}
    </div>
    <div class="row">
      {block name='hook_footer_after'}
        {hook h='displayFooterAfter'}
      {/block}
    </div>
  </div>
</div>
</div>

<div id="footer-copyright">
	<div class="container">
		<div class="row">
			<div class="col-sm-6">
				<div class="copyright-text">
					<p>
						Copyright © 2024
						<a href="https://www.yarnstreet.com">Yarnstreet</a>
					</p>
				</div>
			</div>
			<div class="col-sm-6">
				<div class="copyright-text ">
					<p class='text-sm-right'>
						{l s='Recreated by:' d='Shop.Theme.Yarn'} KubekZTwoimNadrukiem
					</p>
				</div>
			</div>
		</div>
	</div>
</div>
